"""
Since the new user-created activities system will be able to do many of the functions Challenges previously did (i.e. users asking others to answer questions, upload photos, etc.), we would like the new Challenge system to focus on getting users to go to (and pose their own) physical, face-to-face meet ups and events. Thus, we would like to rename "Challenges" as "Crowd!"

Users would open the "Crowd!" page and be presented with two options: either to "Rally a Crowd" or "Join a Crowd."

If a user chooses "Rally a Crowd" they can then essentially create a face-to-face event that they'd like other users to come to (much as users can create Challenges in the existing system.) A user gets an initial points bonus for creating an event. The fields a user is presented with if they choose "Rally a Crowd" are:

-Name the Crowd (the title of the event)
-Upload an Image
-What do you want to accomplish?
-Where? (location of event)
-When? (time of event)
-Confirmation Code

The confirmation code will be a user-created code that will then be given out to people at the actual event. This will later confirm whether or not someone actually attended this event.

Once a user has created an event (or: "Crowd"), it is then displayed in the "Join a Crowd" section. This is a list of all the events (or: "Crowds") that have been created. Here, users can see the information on upcoming or past crowds, comment/ask questions about them, and join them. The number of people who have joined a crowd is always displayed next to its title.

In each each "Crowd" event is a link or button that says "I was a part of this crowd." This opens up a form for a user to type in the confirmation code that they received if they actually attended this event. If this is the correct code, then this user gets a infusion of points and their name is listed under the event as having attended. The creator of the event gets a small point bonus for every confirmed user who attended the event.


To run through an example:

I click "Rally a Crowd" and create an event that I title "Rally For Locally-Produced Food." I write up a description, upload a photo, set the time and location, and choose "eathealthy" as the confirmation code. I click submit, then get an infusion of 25 points, and the crowd event now appears in the "Join a Crowd" section.

You are searching through the "Join a Crowd" section and come across the crowd event I created. You are interested in it, but have a question about whether or not there will be free water there. So you ask this question (in the form of a comment). I respond to your comment and confirm that, yes, there will be free water (nobody gets any points for this exchange). You decide that you want to join the crowd, so you click the button titled "Join." By joining, you have increased the number of people in that crowd, and will receive a notification for when the event is about to happen. 

At the actual physical event, you are given the confirmation code ("eathealthy") and are told to enter this code on the site if you want the point bonus for attending the event. You get home and click the "I was part of this crowd" link in the crowd event, and then type in the code in a form. The system then confirms that you attended this event, and displays your name with the others who have confirmed that they were a part of this crowd. 

For your confirmation that you were a member of this crowd, you get 50 points, and I, the creator of the crowd, get a bonus of 5 points. 
"""
