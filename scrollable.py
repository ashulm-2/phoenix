#"C:\Program Files\Google\Chrome\Application\chrome.exe" https://faculty.phoenix.edu --remote-debugging-port=9222 --user-data-dir="C:/Users/ashul/AppData/Local/Google/Chrome/User Data/Default"

import sys
import time
import datetime
import subprocess
from prompt import R
from welcome import WM
from summatives import SummativeRubrics
from newsummatives import NewSummativeRubrics

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the desired capabilities
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

"""
command = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
args = "https://faculty.phoenix.edu, --remote-debugging-port=9222, --user-data-dir=\"C:\\Users\\ashul\\AppData\\Local\\Google\\Chrome\\User Data\\Default\""

subprocess.run([command, args], capture_output=True, text=True)
"""

# Create the WebDriver instance
driver = webdriver.Chrome(options=options)

import tkinter as tk
from tkinter import ttk, font



 
  
#scrolling functions
def start_scroll(event):
  root.last_y = event.y

def do_scroll(event):
  delta_y = root.last_y - event.y
  root.canvas.yview_scroll(int(delta_y), "units")
  root.last_y = event.y

def bind_mouse_scroll(widget):
  widget.bind_all("<MouseWheel>", on_mousewheel_windows)

def on_mousewheel_windows(event):
  root.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
#end of scrolling functions


#right_frame functions
def Clear(): #clear the current frame of all elements
  for widget in scrollable_frame.winfo_children():
    widget.destroy()



root = tk.Tk()
root.title("Phoenix Grader")
root.state("zoomed")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(0, weight=1)
    
    

    


# Right Pane
right_frame = ttk.Frame()
right_frame.grid(row=0, column=1, sticky="nswe")

canvas = tk.Canvas(right_frame)
scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
  "<Configure>",
  lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

#for i in range(50):
#  ttk.Label(scrollable_frame, text=f"Scrollable content {i+1}").pack(pady=5)

# Mouse wheel scroll binding
bind_mouse_scroll(canvas)

# Drag-to-scroll setup
canvas.bind("<ButtonPress-1>", start_scroll)
canvas.bind("<B1-Motion>", do_scroll)
root.canvas = canvas
root.last_y = 0



# Left Pane
left_frame = ttk.Frame(root, padding=10)
left_frame.grid(row=0, column=0, sticky="nswe")

# Sidebar buttons for navigation
"""Switching tabs"""
def PrintTitle():
  try:
    TitleLabel.config(text = driver.title)
  except Exception as e:
    print(e)
    TitleLabel.config(text="error")
    
def SwitchTab():
  chwd = driver.window_handles
  p = driver.current_window_handle
  for i,w in enumerate(chwd):
    if w == p:
      j = (i+1) % len(chwd)
      driver.switch_to.window(chwd[j])
      break
  PrintTitle()
  

tk.Button(left_frame, text="Switch Tab", command=SwitchTab, width=20, bg="#444", fg="white").pack(pady=10)

TitleLabel = tk.Label(left_frame, text="", wraplength=200)
TitleLabel.pack(pady=10)
PrintTitle()

"""end of Switching Tabs"""

######################################################

"""Grading Interactive Overviews"""
IOValue = None
def GradeIO():
  global IOValue
  """
  this function runs and sets all the grades for the interactive overviews
  """
  #scroll to the bottom of the page so it shows all the students
  bottom = driver.find_element(By.CSS_SELECTOR,"div[class='page-size-component']")
  driver.execute_script("arguments[0].scrollIntoView(true)",bottom)
  time.sleep(1)
  AllInputs = driver.find_elements(By.CSS_SELECTOR,"input[type='text'][placeholder='--']")
  V = IOValue.get()

  for a in AllInputs:
    time.sleep(0.5)
    try: #try to add scores to all the elements  
      a.send_keys(V)
      a.send_keys(Keys.ENTER)
    except:
      print(a) 
      

def DisplayIO():
  """ 
  Content for Interactive Over Screen
  """
  global IOValue
  tk.Label(scrollable_frame, text="Navigate to the Interactive Overview page", font=("Arial", 20)).pack(pady=20)
  tk.Label(scrollable_frame, text="Pick the point value of the assignment, and then hit enter.", font=("Arial", 15)).pack(pady=20)
  IOValue = ttk.Combobox(scrollable_frame, values=["4", "5","10"])
  IOValue["state"] = "readonly"
  IOValue.pack(pady=10)
  IOValue.set("4")

  tk.Button(scrollable_frame, text="Enter", command=GradeIO,width=20).pack(pady=20)

  IOMessage = """I am just following up on your "Interactive Overview" response from this where you weren't able to say that you were confident with the material. That is totally fine, and I appreciate your honesty. I just wanted to reach out and ask if there's anything I can help with to increase that confidence level.\n\nI hope all is well.\n\nBest,\nDrew  """

  IOText = tk.Text(scrollable_frame, wrap="word")
  IOText.insert("1.0", IOMessage)
  IOText.config(state="disabled")
  IOText.pack(pady=20)






tk.Button(left_frame, text="Grade Interactive Overviews", command= lambda :(Clear(), DisplayIO()), bg="#444", fg="white").pack(pady=10) #this lambda function allows us to run Clear and then run Display afterwards


"""end of Grading Interactive Overviews"""

###########################################

"""Grading Discussion"""

def on_button_click(i):
  global AllPostsToggle

  #P is the amount of points discussion is worth; most times it is worth 30 points, but other times it is worth 4 points
  P = float(DiscussionValue.get("1.0", "end-1c"))

  Score = driver.find_elements(By.CSS_SELECTOR, "input[type='text'][placeholder='--']")

  for s in Score:
    try:
      TP = R[i][3]*P
      if AllPostsToggle.get(): #this means we need to deduct for all posts being on the same day
        TP -= .125*P
      s.click()
      s.send_keys(str(TP))
      s.send_keys(Keys.ENTER)
      break
    except Exception as e:
      pass
  
  if AllPostsToggle.get(): #reset it to "No" -- I don't think this is working....
    AllPostsToggle.set(False)
    ToggleButton.config(text=f"{AllPostsToggle.get()}")

  Feedback = driver.find_element(By.CSS_SELECTOR, "bb-svg-icon[icon='add-feedback']")
  Feedback.click()
  FB = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-placeholder='Students see your feedback when you post grades']"))
  )

  Message = R[i][1] #this is the message explaining the grade
  if AllPostsToggle.get(): #this is if all their posts were done on the same day
    Message += "\n\nAlso, all of your posts were on the same day, so there is a 12.5% deduction.  Make sure you spread your posts out over two separate days, per UOP policy."
  FB.send_keys(Message)

  Save = driver.find_element(By.CSS_SELECTOR, "button[data-analytics-id='engagement.feedbackAuthoring.components.feedbackBody.content.primaryFeedback.graderFeedback.feedbackEditor.save']")
  Save.click()

  #time.sleep(1)

  

  Next = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[analytics-id='course.engagement.nextSubmission.link']"))
  )
  Next.click()
  
DiscussionValue = None
AllPostsToggle = None
def DisplayDiscussion():
  global DiscussionValue, AllPostsToggle
  AllPostsToggle = tk.BooleanVar(value=False)
  tk.Label(scrollable_frame, text="Choose the point value associated with this discussion assignment", font=("Arial", 20)).grid(row=0, column=0, columnspan=10)

  DiscussionValue = tk.Text(scrollable_frame, height=1, width=4)
  DiscussionValue.grid(row=1, column=0, columnspan=10)
  DiscussionValue.insert("1.0", "40")



  # Different buttons for participation
  data = [
    [ ["All Good","40"], ["Credited, but replies need more","401"]],
    [ ["Combined Replies","300"],
      ["Initial Reply Late", "301"], 
      ["Missing Second Reply", "302"]],
    [ ["Late Thursday, Combined Replies", "200"],
      ["Missing Replies", "201"],
      ["Replies, but cannot credit", "202"],
      ["Late Thursday, missing 2nd reply", "203"],
      ["Light Initial, cannot credit replies", "204"]],
    [ ["Late Thursday, cannot credit replies", "100"],
      ["Only initial post, but late", "101"]],
    [ ["No Credit", "01"]]
  ]
  
  # Create the table with buttons for discussion
  Bold = font.Font(weight="bold")
  for row_index, row_data in enumerate(data):
    tk.Label(scrollable_frame, text=f"{25*(4-row_index)}%",font=Bold).grid(row=row_index+2, column=0)
    for col_index, cell_data in enumerate(row_data):
      # Create a button for each cell
      button = tk.Button(
        scrollable_frame,
        text=cell_data[0],
        command=lambda cd = cell_data[1]:on_button_click(cd),
        width=30,  # Adjust button width
        height=2   # Adjust button height
      )
      button.grid(row=row_index+2, column=col_index+1, padx=5, pady=5)
    
    
  ToggleButton = ttk.Checkbutton(
    scrollable_frame,
    text="False",
    variable=AllPostsToggle,
    command=lambda: ToggleButton.config(text=f"{AllPostsToggle.get()}"),
    style="Toggle.TButton"
  )
  ToggleButton.grid(row=7,column=1, pady=10)
  tk.Label(scrollable_frame, text="All Posts One Day?", font=Bold).grid(row=7, column=0)

  
  

tk.Button(left_frame, text="Grade Discussion", command=lambda :(Clear(),DisplayDiscussion()), bg="#444", fg="white").pack(pady=10)
                            
                            
                            
                            
"""end of Grading Discussion"""

##########################################

"""List of Summative Assessments"""

def DisplayListofSAs():
  for count,A in enumerate(sorted(SummativeRubrics)):
    tk.Button(scrollable_frame, text=A, command=lambda x=A: (Clear(),DisplaySA(x))).pack(pady=5)
  for count,A in enumerate(sorted(NewSummativeRubrics)):
    tk.Button(scrollable_frame, text=A, command=lambda x=A: (Clear(),NewDisplaySA(x))).pack(pady=5)
                          
tk.Button(left_frame, text="Grade Summative Assessments", command=lambda :(Clear(),DisplayListofSAs()), bg="#444", fg="white").pack(pady=10)

"""end of List of Summative Assessments"""

#######################################


"""Basic Grading of Summative Assessments"""

NewSARubrics = ["MTH219Week2"]

TKVars = []
def DisplaySA(Course):   
  global TKVars

  tk.Label(scrollable_frame, text="Grading for " + Course).pack(pady=10)
  TKVars = [] #this holds the information from all the radio buttons
  for part in SummativeRubrics[Course]:
    var = tk.IntVar(value=0)
    TKVars.append(var)
    tk.Label(scrollable_frame, text = f"Part {part}:").pack(pady=2, anchor="w")
    for grade in SummativeRubrics[Course][part]:
      tk.Radiobutton(scrollable_frame, 
        text=f"{SummativeRubrics[Course][part][grade][0]}", 
        value=grade, 
        variable=var,
        #command=lambda: SelectedRadio(Course)
      ).pack(pady=2, anchor="w")
    tk.Label(scrollable_frame, text="=================================").pack(pady=5)

  tk.Button(scrollable_frame,
    text="Submit Grade",
    command=lambda: SelectedRadio(Course)
  ).pack(pady=10, anchor="w")

def NewDisplaySA(Course):
  global TKVars

  tk.Label(scrollable_frame, text="Grading for " + Course).pack(pady=5)
  tk.Label(scrollable_frame, text="If the student made a mistake and we should deduct points, check the button.  So an unchecked button means they did that part correctly.").pack(pady=10)
  TKVars = [] #this holds the information from all the check buttons
  for part in NewSummativeRubrics[Course]:
    tk.Label(scrollable_frame, text = f"Part {part}:").pack(pady=2, anchor="w")
    for count in NewSummativeRubrics[Course][part]:
      var = tk.IntVar(value=0)
      TKVars.append((part,count,var))
      tk.Checkbutton(scrollable_frame, 
        text=f"{NewSummativeRubrics[Course][part][count][0]} (-{NewSummativeRubrics[Course][part][count][1]} points)", 
        variable=var,
      ).pack(pady=2, anchor="w")
    tk.Label(scrollable_frame, text=40*"=").pack(pady=5, anchor="w")
    
  tk.Button(scrollable_frame,
    text="Submit Grade",
    command=lambda: SelectedCheckButtons(Course)
  ).pack(pady=10, anchor="w")
  
def WhichButton(value):
  #this function helps us determine which grade pill to set, based on the value; the four different value intervals are 90-100 70-89, 50-69, 0-0
  if value >= 90:
    return 0
  elif value >= 70:
    return 1
  elif value >= 50:
    return 2
  else:
    return 3
  
def SelectedCheckButtons(Course):
  """
  this function is run when you are ready to submit the grade
  """

  Parts = len(NewSummativeRubrics[Course])
  Message = ""
  Scores = {i:100 for i in range(1,Parts+1)}
  
  for i, (part,count,var) in enumerate(TKVars, start=1):
    #first we loop through all the Checkbutton variables (TKVars) and grab the messages and values associated to each of them
    if (var.get() == 1): #that means the button was selected
      #print(part,var,var.get())
      Message += NewSummativeRubrics[Course][part][count][2] + "\n"
      Scores[part] -= NewSummativeRubrics[Course][part][count][1]
  
  if Message == "":
    Message = "Fantastic job with this assignment!  You did everything perfectly!"
  else:
    Message += "Everything else looks good!"

  #this part sets the message for the student
  FB = driver.find_element(By.CSS_SELECTOR, "div[data-placeholder='Enter your feedback']")
  FB.send_keys(Message)
  Save = driver.find_element(By.CSS_SELECTOR, "button[data-analytics-id='attemptGrading.page.body.overallFeedback.saveButton']")
  Save.click()
  
  #now we loop through all the grade pills and set the ones we marked above
  D = driver.find_elements(By.CSS_SELECTOR,"div[class^='makeStyleslabel-0-2-']")
  for part,v in Scores.items():
    D[4*(part-1)+WhichButton(v)].click()
    time.sleep(0.25)
    Input = driver.find_elements(By.CSS_SELECTOR, "input[aria-label^='Add a value']")
    for i in Input:
      i.send_keys(str(v))
      i.send_keys(Keys.ENTER)
    
  #the next line resets radio buttons for the next student 
  Clear()
  NewDisplaySA(Course)

"""end of Basic Grading of Summative Assessments"""

#########################################


"""Create Announcements"""

from announcements import *

def PostAnnouncements():
  wait = WebDriverWait(driver,10)
  """
  this function runs to post announcements
  """
  CourseNumber = int(CN.get())
  FT = datetime.datetime.strptime(FirstThursday.get("1.0", "end-1c"),"%m/%d/%y")
  FM = FT + datetime.timedelta(days=4) #FM stands for FirstMonday
  FirstTuesday = FT + datetime.timedelta(days=-2)
  #print(CourseNumber, FT)
  #print(type(CourseNumber), type(FT))
  
  #post the welcome message
  PostIndividualAnnouncement(
    subject="Welcome and Instructor Information",
    message=WM[CourseNumber],
    ScheduleDate = FirstTuesday.strftime("%m/%d/%y"))
    

  #post AI announcements
  
  PostIndividualAnnouncement(
    subject="UOP Policy on AI Tools",
    message="Hi everyone,\n\nThis is a reminder that University of Phoenix has a policy that covers appropriate use of artificial intelligence (AI) in our classes. This is included in the Academic Policies document under Tools & Resources.\n\nIf you use an artificial intelligence (AI) tool when preparing an assignment or discussion response, make sure to include a statement that describes how you used it and remember: 1) the majority of assignments must be your own writing; 2) you must quote and cite any content generated by the AI tool; and 3) you must verify the accuracy of the content generated by the AI tool.\n\nTake a moment to read the UOPX Philosophy Statement on Generative AI[1] and watch How to Meet University Requirements When Using Generative AI[2]. It’s less than two minutes and provides a clear description of how to make sure you’re meeting requirements if you use generative AI for an assignment or discussion post.\n\nIt’s important to ensure you understand how to use AI effectively and ethically. If you have any questions or concerns regarding the use of AI in our class, please let me know.\n\nBest,\nDrew\n\n [1]https://multimedia.phoenix.edu/cms/202340709 \n[2]https://player.vimeo.com/video/1053433552",
    ScheduleDate = FirstTuesday.strftime("%m/%d/%y"))
    
  PostIndividualAnnouncement(
    subject="Further Generative AI Information",
    message="Hi everyone,\n\nAs the course gets started, I wanted to remind you of a UOP policy regarding generative AI (like ChatGPT, DeepSeek, and the like).  You might have noticed that I posted an announcement with the official UOP policy regarding generative AI, but I wanted to add my two cents worth.  If you simply use these tools to create your own posts, then this is a violation of the university's policies and you're cheating yourself out of knowledge by not thinking about the material, and you're cheating your classmates out of the opportunity to learn from you and your experiences.  In other words, I would like our discussions to be genuine and **I want to hear from you**!\n\nPlease do not get me wrong.  I think that there are some excellent uses of these generative AI tools.  In fact, I run research groups where we try to create our own tools for specific tasks.  In particular, I have created computer bots to play games like checkers, chess, mancala, and minesweeper, as well as recognizing handwriting and turning it into digital content.  [Feel free to ask me about any of this if you're interested.]  I am definitely a proponent of pushing these AI tools forward, but I am asking you to use them appropriately (and sparingly!) when it comes to classroom discussions.\n\nMy own policy is if you use AI tools inappropriately according to UOP's policies, I will write you a private message warning asking you to rewrite the post.  If I catch it a second time, then there will be loss of points involved with no chance of making those points back up.  So the easy solution is to use these tools in an appropriate manner (which includes direct citations and a limited use of the tool when writing your posts) because their use is easy to spot and there are other tools that help instructors determine a post's origins.\n\nIf you have any questions or concerns, please do not hesitate to ask me.  I look forward to fruitful classroom discussions!\n\nBest,\nDrew",
    ScheduleDate = FirstTuesday.strftime("%m/%d/%y"))
  
  N = len(AnnDict[CourseNumber])


  for Week in range(1,N+1):
    time.sleep(1)
    Offset = 7*(Week-1)
    Delta = datetime.timedelta(days=Offset)
    NewDate = FT + Delta
    
    PostIndividualAnnouncement(
      subject="Week {} Discussion Reminder".format(Week),
      message="Hi everyone!\n\nI hope Week {} is going well for you.  Don't forget that your initial response to this week's discussion is due by the end of the day today.  Don't hesitate to ask me if you have any questions!\n\nBest,\nDrew".format(Week),
      ScheduleDate=NewDate.strftime("%m/%d/%y"))
    



  for Week in range(1,N+1):
    time.sleep(1)
    Offset = 7*(Week-1)
    Delta = datetime.timedelta(days=Offset)
    NewDate = FM + Delta
    
    PostIndividualAnnouncement(
      subject="End of Week {} Reminder".format(Week),
      message="Hi everyone!\n\nWe're nearing the end of Week {}, which means its time to get those assignments in order.  Please finish up your two replies to me or your classmates, and finish the remaining assignments due by the end of the week (today) which include the following assignments:\n\nInteractive Overview (be honest!)\n".format(Week) + AnnDict[CourseNumber][Week] + "\n\nDon't hesitate to ask me if you have any questions!\n\nBest,\nDrew",
      ScheduleDate=NewDate.strftime("%m/%d/%y"))
      
def ScoresPublishedAnnouncement():
  CourseNumber = int(CN.get())
  WeekNumber = WW.get()
  if int(WeekNumber) == len(AnnDict[CourseNumber]): #this means it is the last week of the course
    Message = "Hello class,\n\nThe final week’s grades are now published. Please look over your scores and my comments. The last day to make any comments about your final grade is Friday night, for I will be posting grades on Saturday morning.\n\nYou also have until Friday to complete any non-participation assignments for credit with a 10% penalty.\n\nIt was a pleasure working with everyone, and I wish you the best of luck with the remainder of your education!\n\nIf you need to contact me after the course ends, please feel free to email me:  ashulman@phoenix.edu.\n\nBest,\nDrew"
    Subject = f"Week {WeekNumber} Grades Posted and Final Grade Information"
  else:
    Message = f"Hello class,\n\nThe week {WeekNumber} scores have been posted.\n\nPlease look over your scores and my comments and let me know if you have any questions or concerns.  In order to see my comments, there is a little box next to your score that you can click and see some information I have left for you.\n\nIf you complete any work (besides participation) between now and the end of the day Friday, I will update your score on Saturday with a 10% late penalty."
    Subject = f"Week {WeekNumber} Grades Posted"
  print(Subject,Message)
  PostIndividualAnnouncement(Subject,Message)


CN = None
WW = None
def DisplayAnnouncements():
  global CN, WW
  tk.Label(scrollable_frame, text="First, navigate to the announcements page of the course.  Next, choose which course the announcements are for.  Finally, type the date of the first Thursday for the course in the form MM/DD/YY.").pack(pady=10)

  CN = ttk.Combobox(scrollable_frame, values=CoursesList)
  CN["state"] = "readonly"
  CN.pack(pady=10)
  CN.set("210")

  FirstThursday = tk.Text(scrollable_frame, height=1, width=10)
  FirstThursday.pack(pady=10)
  FirstThursday.insert("1.0", "MM/DD/YY")

  tk.Button(scrollable_frame, text="Enter", command=PostAnnouncements,width=20).pack(pady=20)

  ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x")

  tk.Label(scrollable_frame,text="To create an announcement for published grades, nagivate to the announcements page, MAKE SURE TO CHOOSE THE CORRECT COURSE NUMBER ABOVE, and choose the week these grades are for.").pack(pady=10)

  WW = ttk.Combobox(scrollable_frame, values=["1", "2", "3", "4", "5","6","7"])
  WW["state"] = "readonly"
  WW.pack(pady=10)
  WW.set("1")

  tk.Button(scrollable_frame, text="Enter", command=ScoresPublishedAnnouncement,width=20, bg="#444", fg="white").pack(pady=20)

tk.Button(left_frame, text="Create Announcements", command= lambda :(Clear(),DisplayAnnouncements()), bg="#444", fg="white").pack(pady=10)


"""end of Create Announcements"""

###########################



Clear()
DisplayIO()

root.mainloop()
