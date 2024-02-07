## Installation and Running
1. open an IDE (recommend: VScode)
2. run the following in the terminal inside the IDE:
```
git clone https://github.com/KalengBalsem/instalyzer.git
```
3. locate the instalyzer file in the terminal:
   ```
   cd instalyzer
   ```
6. install the dependencies by running this command in the terminal:
```
pip3 install -r requirements.txt
```
7. run this command in the terminal to run the server in localhost:
```
python3 main.py

PS C:\Users\balse\Documents\VScode\instalyzer> python main.py

# output:
Created Database!
 * Serving Flask app 'application'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
Created Database!
 * Debugger is active!
 * Debugger PIN: 102-884-233
```
8. open the localhost link -> 127.0.0.1:5000
9. done

## Feature
Enter an Instagram (IG) username to generate the following output:
- Main user profile information (user_id, username, full_name, posts_count, followers, following, bio, category)
- IG posts data (likes, comments, hashtags, tagged user, timestamp (upload time), etc.)

Data visualizations:
- Most popular upload day
- Most popular upload time
- Line plot of recent posts' performance (based on likes/comments)
- Note: the user can click on the data, then be given a link directing to that post.
- Top hashtags
- Top caption words
- List of links to Most Liked Posts and Most Commented Posts
