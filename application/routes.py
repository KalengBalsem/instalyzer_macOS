from flask import render_template, Blueprint, request, session, redirect, url_for, json
from .models import Profile, Post                       # importing the database
from . import db

from .data_parser import parse_profile, parse_posts     # importing parser
from .data_scraper import scrape_data, scrape_more      # to run scraper on different file
from .data_analyzer import analyze_data                 # to analyze data
import os.path                                          # to check whether the data exists in the scraped_data folder


routes = Blueprint('routes', __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        return "<h1>an error has occured</h1>"
    elif request.method == "POST":
        session['ig_username'] = request.form['ig_username']
        session['iteration'] = int(request.form['iteration'])
        return redirect(url_for('routes.preparing_data'))
    
@routes.route('/preparing-data/')
def preparing_data():

    # defining ig_username
    ig_username = session.get('ig_username', None)
    ####

    # iteration
    iteration = session.get('iteration', None)
    ####

    # checking whether the data already exists
    for iter in range(iteration+1):
        path = f'scraper/scraped_data/{ig_username}{iter}.json'
        data_exists = os.path.isfile(path)
    ####

    # create update condition if there's None
    if session.get('update_data', None) is None:
        session['update_data'] = False
    update_data = session.get('update_data', None)
    ####

    # getting the data, redirect to show data

    # defining go to show-data to make life easier
    show_data_url = url_for('routes.show_data', ig_username=ig_username)
    ###

    if data_exists and not update_data:
        return redirect(show_data_url)
    elif iteration == 0:
        scraping_success = scrape_data(ig_username)
        if scraping_success:
            return redirect(show_data_url)
        else:
            return "<h3>Failed to get the data. Make sure the IG Username is valid.</h3>"
    elif iteration > 0:
        scraping_success = scrape_data(ig_username)
        more_scraping_success = scrape_more(ig_username, iteration)
        if scraping_success and more_scraping_success:
            return redirect(show_data_url)
        elif scraping_success:
            print('Failed to get more data iteration.')
            return redirect(show_data_url)
        else:
            return "<h3>Failed to get the data. Make sure the IG Username is valid.</h3>"
    ####

@routes.route('/show-data/<ig_username>/')
def show_data(ig_username):

    # updating session if ig_username changed using url and the data_exists.
    if session.get('ig_username', None) != ig_username:
        return redirect(url_for('routes.index'))

    iteration = session.get('iteration', None)
    ####

    # recheck if the data exists (in case user modifying the username in web query straight away)
    available_post_data = 0
    for iter in range(iteration+1):
        path = f'scraper/scraped_data/{ig_username}{iter}.json'
        data_exists = os.path.isfile(path)
        if iter == 0 and data_exists:
            profile_data_exists = data_exists

        if iter > 0 and data_exists:
            available_post_data += 1
    ####

    # defining update_data and if update_available (data is already in the database)
    update_data = session.get('update_data', None)
    update_available = False
    ####

    # getting profile and post
    found_profile = Profile.query.filter_by(username=ig_username).first() # will return None if username is not found
    # below is to support iteration feature
    if found_profile:
        found_post = Post.query.filter_by(owner_id=found_profile.id).all()
        requested_post = (iteration+1)*12
        if len(found_post) < 12:
            found_more_post = True
        else:
            found_more_post = len(found_post) >= requested_post
    else:
        found_post = []
        found_more_post = False
    ####

    # getting and modifying the database
    if profile_data_exists:
        if found_profile and found_more_post and not update_data:
            ig_profile = found_profile
            update_available=True
        else:
            path = f'scraper/scraped_data/{ig_username}0.json'
            with open(path, 'r',  encoding="utf8") as file:
                data = json.load(file)
                try:
                    profile_data = parse_profile(data)
                except:
                    return "<h3>Username not Found.</h3>"
            
            # updating data: remove the data first before adding the new one.
            if update_data:
                if found_post: # in case user doesnt have any post
                    for i in found_post:
                        db.session.delete(i)
                if found_profile:
                    db.session.delete(found_profile)
                db.session.commit()
            ####
            
            # instantiating profile and posts data
            if not found_profile or update_data:
                profile = Profile(
                                user_id = profile_data['id'],
                                username = profile_data['username'],
                                full_name = profile_data['full_name'],
                                category = profile_data['category'],
                                posts_count = profile_data['posts_count'],
                                followers = profile_data['followers'],
                                following = profile_data['following'],
                                profile_picture = profile_data['profile_picture'],
                                no_of_highlights = profile_data['no_of_highlights'],
                                bio = profile_data['bio'],
                                bio_link = profile_data['bio link'],
                                is_private = profile_data['is_private']
                            )

                # adding profile_data to database + commiting changes
                db.session.add(profile)
                db.session.commit()

            # assigning the profile data
            ig_profile = Profile.query.filter_by(username=ig_username).first()
            ####

            # defining post_data function (as database object) for reusability
            def post_func(post_data):
                post = Post(
                                    post_id = post_data['post_id'],
                                    post_type = post_data['post_type'],
                                    display_url = post_data['display_url'],
                                    caption = post_data['caption'],
                                    hashtags = ' '.join(post_data['hashtags']),
                                    likes_count = post_data['likes_count'],
                                    comments_count = post_data['comments_count'],
                                    url = post_data['url'],
                                    timestamp = post_data['timestamp'],

                                    owner_id = ig_profile.id
                            )
                return post
            ####
            
            # looping in posts_data and send it to the database
            if not found_more_post or update_data:
                start = int(len(found_post) / 12)       # to start from 0
                end = available_post_data + 1           # to include the last iteration (taken from the data_exists loop line 86)
                for iter in range(start, end):
                    path = f'scraper/scraped_data/{ig_username}{iter}.json'
                    with open(path, 'r',  encoding="utf8") as file:
                        data = json.load(file)
                        more_posts_data = parse_posts(data, ig_username)
                    
                    for i, post_data in more_posts_data.items():
                        post = post_func(post_data)
                        db.session.add(post)
                # commiting changes (more posts_data)
                db.session.commit()
            ####
    else:
        return redirect(url_for('routes.index'))
    
    # defining ig_profile, send it to templates
    ig_profile = Profile.query.filter_by(username=ig_username).first()
    ####

    # analyze data + data visualization
    analyzed_data = analyze_data(ig_username, iteration)
    ####

    # reset session
    session['update_data'] = False
    ####

    return render_template("data.html", ig_profile=ig_profile, update_available=update_available, analyzed_data=analyzed_data)

@routes.route('/update-data')
def update_data():
    session['update_data'] = True  
    return redirect(url_for('routes.preparing_data'))