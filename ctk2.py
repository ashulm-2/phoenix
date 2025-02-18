#"C:\Program Files\Google\Chrome\Application\chrome.exe" https://faculty.phoenix.edu --remote-debugging-port=9222 --user-data-dir="C:/Users/ashul/AppData/Local/Google/Chrome/User Data/Default"

import tkinter as tk
from tkinter import ttk, font
from summatives import SummativeRubrics

import sys
import time
import datetime
import subprocess
from prompt import R
from welcome import WM

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
#time.sleep(3)


# Function to show a frame
def show_frame(frame):
  frame.tkraise()

def ClearFrame(frame): #clear the current frame of all elements
  for widget in frame.winfo_children():
    widget.destroy()
  


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



TKVars = []

def AssignGradeToBubblev1(part, value):
  if value >= 90:
    Top = driver.find_elements(By.XPATH, "//*[contains(text(), '90 - 100%')]")
  elif value >= 70:
    Top = driver.find_elements(By.XPATH, "//*[contains(text(), '70 - 89%')]")
  elif value >= 50:
    Top = driver.find_elements(By.XPATH, "//*[contains(text(), '50 - 69%')]")
  else:
    Top = driver.find_elements(By.XPATH, "//*[contains(text(), '0 - 0%')]")
  
  count = 1
  for t in Top:
    if count == part:
      t.click()
      time.sleep(0.25)
      if value >= 90:
        In = driver.find_elements(By.CSS_SELECTOR, "input[placeholder='90 - 100']")
      elif value >= 70:
        In = driver.find_elements(By.CSS_SELECTOR, "input[placeholder='70 - 89']")
      elif value >= 50:
        In = driver.find_elements(By.CSS_SELECTOR, "input[placeholder='50 - 69']")
      else:
        In = driver.find_elements(By.CSS_SELECTOR, "input[placeholder='0 - 0']")
      for i in In:
        i.send_keys(str(value))
        i.send_keys(Keys.ENTER)
        return 1
    count += 1
    
def WhichButton(value):
  #this function helps us determine which grade pill to set, based on the value; the four different value intervals are 90-100 70-89, 50-69, 0-0
  if value >= 90:
    return 1
  elif value >= 70:
    return 2
  elif value >= 50:
    return 3
  else:
    return 4
  

def SelectedRadio(Course):
  """
  this function is run when you are ready to submit the grade
  """
  Message = ""
  Values = []
  for i, var in enumerate(TKVars, start=1):
    #first we loop through all the radio button variables (TKVars) and grab the messages and values associated to each of them
    Message += SummativeRubrics[Course][i][var.get()][2] + "\n"
    V = SummativeRubrics[Course][i][var.get()][1]
    Values.append((4*(i-1) + WhichButton(V), V)) #Values contains tuples where the first entry is which of the grading pills you are setting the value for (since we loop through all of them), and the second entry is the value to assign to that pill 

  #this part sets the message for the student
  FB = driver.find_element(By.CSS_SELECTOR, "div[data-placeholder='Enter your feedback']")
  FB.send_keys(Message)
  Save = driver.find_element(By.CSS_SELECTOR, "button[data-analytics-id='attemptGrading.page.body.overallFeedback.saveButton']")
  Save.click()
  
  #now we loop through all the grade pills and set the ones we marked above
  D = driver.find_elements(By.CSS_SELECTOR,"div[class^='makeStyleslabel-0-2-']")
  print(Values)
  for i,v in Values:
    D[i-1].click()
    time.sleep(0.25)
    Input = driver.find_elements(By.CSS_SELECTOR, "input[aria-label^='Add a value']")
    for i in Input:
      i.send_keys(str(v))
      i.send_keys(Keys.ENTER)
    
  #the next line resets radio buttons for the next student 
  SARubric(Course)
  


def SARubric(Course):
  show_frame(SA)
  global TKVars
  ClearFrame(SA)
  tk.Label(SA, text="Grading for " + Course).grid(row=0, column=0)
  TKVars = [] #this holds the information from all the radio buttons
  Row = 1
  for part in SummativeRubrics[Course]:
    var = tk.IntVar(value=0)
    TKVars.append(var)
    tk.Label(SA, text = f"Part {part}:").grid(row=Row, column=0, sticky="W")
    Row += 1
    #col = 1
    for grade in SummativeRubrics[Course][part]:
      tk.Radiobutton(SA, 
        text=f"{SummativeRubrics[Course][part][grade][0]}", 
        value=grade, 
        variable=var,
        #command=lambda: SelectedRadio(Course)
      ).grid(row=Row, column=0, sticky="W")
      Row += 1
      #col += 1
    tk.Label(SA, text="=================================").grid(row=Row, column=0,sticky="W")
    Row += 1

  tk.Button(SA,
    text="Submit Grade",
    command=lambda: SelectedRadio(Course)
  ).grid(row=Row, column=0)
    

def GradeIO():
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
    try: #try to add scores to all the elements  
      a.send_keys(V)
      a.submit()
    except:
      print(a) 
      
def PostIndividualAnnouncement(subject,message,ScheduleDate=None):
  wait = WebDriverWait(driver,10)
  try:
    CA = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[aria-label='Create Announcement']")))
    CA.click()
  except:
    print("Couldn't create an announcement")
    #sys.exit()

  Title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[placeholder='Type an announcement title']")))
  Title.send_keys(subject)

  Ann = driver.find_element(By.CSS_SELECTOR,"[data-placeholder='Type an announcement message']")
  Ann.send_keys(message)
  
  if ScheduleDate is not None:
    SA = driver.find_element(By.CSS_SELECTOR,"[id='schedule-announcement-checkbox']")
    driver.execute_script("arguments[0].scrollIntoView(true)",SA)
    SA.click()
    time.sleep(0.5)

    Date = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[class='date-input']")))
    Date.send_keys(Keys.CONTROL + "a")
    Date.send_keys(Keys.DELETE)
    Date.send_keys(ScheduleDate)

    Time = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[class='time-input']")))
    Time.send_keys(Keys.CONTROL + "a")
    Time.send_keys(Keys.DELETE)
    Time.send_keys("2:30 AM")
  else: #send email announcement
    Btn = driver.find_element(By.CSS_SELECTOR,"[id='send-email-checkbox']")
    Btn.click()
    

  Post = driver.find_element(By.CSS_SELECTOR,"button[data-analytics-id='course.announcements.detailPanel.post.button']")
  Post.click()
  
def ScoresPublishedAnnouncement():
  WeekNumber = WW.get()
  if WeekNumber == "5":
    Message = "Hello class,\n\nThe final week’s grades are now published. Please look over your scores and my comments. The last day to make any comments about your final grade is Friday night, for I will be posting grades on Saturday morning.\n\nYou also have until Friday to complete any non-participation assignments for credit with a 10% penalty.\n\nIt was a pleasure working with everyone, and I wish you the best of luck with the remainder of your education!\n\nIf you need to contact me after the course ends, please feel free to email me:  ashulman@phoenix.edu.\n\nBest,\nDrew"
    Subject = "Week 5 Grades Posted and Final Grade Information"
  else:
    Message = f"Hello class,\n\nThe week {WeekNumber} scores have been posted.\n\nPlease look over your scores and my comments and let me know if you have any questions or concerns.  In order to see my comments, there is a little box next to your score that you can click and see some information I have left for you.\n\nIf you complete any work (besides participation) between now and the end of the day Friday, I will update your score on Saturday with a 10% late penalty."
    Subject = f"Week {WeekNumber} Grades Posted"
  #print(Subject,Message)
  PostIndividualAnnouncement(Subject,Message)



def PostAnnouncements():
  wait = WebDriverWait(driver,10)
  """
  this function runs to post announcements
  """
  CourseNumber = int(CN.get())
  FT = datetime.datetime.strptime(FirstThursday.get("1.0", "end-1c"),"%m/%d/%y")
  FM = FT + datetime.timedelta(days=4) #FM stands for FirstMonday
  #print(CourseNumber, FT)
  #print(type(CourseNumber), type(FT))
  
  #post the welcome message
  PostIndividualAnnouncement(
    subject="Welcome and Instructor Information",
    message=WM[CourseNumber],
    ScheduleDate = FM.strftime("%m/%d/%y"))

  for Week in range(1,6):
    time.sleep(1)
    Offset = 7*(Week-1)
    Delta = datetime.timedelta(days=Offset)
    NewDate = FT + Delta
    
    PostIndividualAnnouncement(
      subject="Week {} Discussion Reminder".format(Week),
      message="Hi everyone!\n\nI hope Week {} is going well for you.  Don't forget that your initial response to this week's discussion is due by the end of the day today.  Don't hesitate to ask me if you have any questions!\n\nBest,\nDrew".format(Week),
      ScheduleDate=NewDate.strftime("%m/%d/%y"))
    



  for Week in range(1,6):
    time.sleep(1)
    Offset = 7*(Week-1)
    Delta = datetime.timedelta(days=Offset)
    NewDate = FM + Delta
    
    PostIndividualAnnouncement(
      subject="End of Week {} Reminder".format(Week),
      message="Hi everyone!\n\nWe're nearing the end of Week {}, which means its time to get those assignments in order.  Please finish up your two replies to me or your classmates, and finish the remaining assignments due by the end of the week (today) which include the following assignments:\n\nInteractive Overview (be honest!)\n".format(Week) + AnnDict[CourseNumber][Week] + "\n\nDon't hesitate to ask me if you have any questions!\n\nBest,\nDrew",
      ScheduleDate=NewDate.strftime("%m/%d/%y"))
      

  

# Main application window
root = tk.Tk()
root.title("Phoenix Grader")
root.state("zoomed")
#root.geometry("600x400")

# Create the main container for layout
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create the sidebar frame
sidebar = tk.Frame(container, bg="#333", width = 500, borderwidth=10)
sidebar.pack(side="left", fill="y", expand=True)

# Create the content area for screens
content_area = tk.Frame(container)
content_area.pack(side="right", fill="both", expand=True)

# Configure the content area for screen stacking
content_area.grid_rowconfigure(0, weight=1)
content_area.grid_columnconfigure(0, weight=1)


# Sidebar buttons for navigation
tk.Button(sidebar, text="Switch Tab", command=SwitchTab, width=20, bg="#444", fg="white").pack(pady=10)

TitleLabel = tk.Label(sidebar, text="", wraplength=200)
TitleLabel.pack(pady=10)
PrintTitle()

tk.Button(sidebar, text="Grade Interactive Overviews", command=lambda: show_frame(IO), bg="#444", fg="white").pack(pady=10)

tk.Button(sidebar, text="Grade Discussion", command=lambda: show_frame(Discussion),
                            bg="#444", fg="white").pack(pady=10)
                          
tk.Button(sidebar, text="Grade Summative Assessments", command=lambda: show_frame(SAButtons), bg="#444", fg="white").pack(pady=10)

tk.Button(sidebar, text="Create Announcements", command=lambda: show_frame(Announcements), bg="#444", fg="white").pack(pady=10)





# Create different frames for screens
#these are the different screens that show on the right side when the sidebar buttons are pressed
main_screen = tk.Frame(content_area, bg="#f0f0f0")
IO = tk.Frame(content_area, bg="#e0f7fa")
Discussion = tk.Frame(content_area, bg="#ffe0b2")
SA = tk.Frame(content_area, bg="#4b9cd3")
SAButtons = tk.Frame(content_area, bg="red")
Announcements = tk.Frame(content_area, bg="green")

# Grid layout to stack frames
for frame in (main_screen, IO, Discussion, SA, SAButtons, Announcements):
    frame.grid(row=0, column=0, sticky="nsew")

# Content for the main screen
label_main = tk.Label(main_screen, text="Main Screen", font=("Arial", 20), bg="#f0f0f0")
label_main.pack(pady=20)



""" 
Content for Interactive Over Screen
"""
tk.Label(IO, text="Navigate to the Interactive Overview page", font=("Arial", 20), bg="#e0f7fa").pack(pady=20)
tk.Label(IO, text="Pick the point value of the assignment, and then hit enter.", font=("Arial", 15), bg="#e0f7fa").pack(pady=20)
IOValue = ttk.Combobox(IO, values=["4", "5"])
IOValue["state"] = "readonly"
IOValue.pack(pady=10)
IOValue.set("4")

tk.Button(IO, text="Enter", command=GradeIO,width=20, bg="#444", fg="white").pack(pady=20)

""" 
End of Content for Interactive Over Screen
"""


  
""" 
Content for Discussion Grading
"""
# Content for Screen 2
tk.Label(Discussion, text="Choose the point value associated with this discussion assignment", font=("Arial", 20), bg="#ffe0b2").grid(row=0, column=0, columnspan=10)

DiscussionValue = tk.Text(Discussion, height=1, width=4)
DiscussionValue.grid(row=1, column=0, columnspan=10)
DiscussionValue.insert("1.0", "40")



# Different buttons for participation
data = [
  [ ["All Good","40"]],
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

# Function to handle button click for participation buttons
def on_button_click(i):

  #P is the amount of points discussion is worth; most times it is worth 30 points, but other times it is worth 4 points
  P = float(DiscussionValue.get("1.0", "end-1c"))
  Feedback = driver.find_element(By.CSS_SELECTOR, "bb-svg-icon[icon='add-feedback']")
  Feedback.click()
  FB = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-placeholder='Students see your feedback when you post grades']"))
  )

  Message = R[i][1] #this is the message explaining the grade
  if AllPostsToggle.get(): #this is if all their posts were done on the same day
    Message += "\n\nAlso, all of your posts were on the same day, so there is a 12.5% deduction.  Make sure you spread your posts out over two separate days, per UOP policy."
  FB.send_keys(Message)
  
  Score = driver.find_elements(By.CSS_SELECTOR, "input[type='text'][placeholder='--']")
  for s in Score:
    try:
      TP = R[i][3]*P
      if AllPostsToggle.get(): #this means we need to deduct for all posts being on the same day
        TP -= .125*P
      s.send_keys(str(TP))
      s.send_keys(Keys.ENTER)
      break
    except:
      pass 

  Save = driver.find_element(By.CSS_SELECTOR, "button[data-analytics-id='engagement.feedbackAuthoring.components.feedbackBody.content.primaryFeedback.graderFeedback.feedbackEditor.save']")
  Save.click()
  
  if AllPostsToggle.get(): #reset it to "No" -- I don't think this is working....
    print("here")
    toggle_action()

  Next = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[analytics-id='course.engagement.nextSubmission.link']"))
  )
  Next.click()
  
  
  


# Create the table with buttons for discussion
Bold = font.Font(weight="bold")
for row_index, row_data in enumerate(data):
  tk.Label(Discussion, text=f"{25*(4-row_index)}%", bg="#ffe0b2", font=Bold).grid(row=row_index+2, column=0)
  for col_index, cell_data in enumerate(row_data):
    # Create a button for each cell
    button = tk.Button(
      Discussion,
      text=cell_data[0],
      command=lambda cd = cell_data[1]:on_button_click(cd),
      width=30,  # Adjust button width
      height=2   # Adjust button height
    )
    button.grid(row=row_index+2, column=col_index+1, padx=5, pady=5)
    
    
    
AllPostsToggle = tk.BooleanVar(value=False)
def toggle_action(): #this is the button for all posts on one day
  global AllPostsToggle
  if AllPostsToggle.get():
    ToggleButton.config(text="Yes")
    AllPostsToggle.set(True)
  else:
    ToggleButton.config(text="No")
    AllPostsToggle.set(False)
    
    
ToggleButton = ttk.Checkbutton(
  Discussion,
  text="No",
  variable=AllPostsToggle,
  command=toggle_action,
  style="Toggle.TButton"
)
ToggleButton.grid(row=7,column=1, pady=10)
tk.Label(Discussion, text="All Posts One Day?", bg="#ffe0b2", font=Bold).grid(row=7, column=0)





"""this will be the content for the summative assessments buttons"""
tk.Label(SAButtons, text="Choose which course/summative assement to grade", bg="#4b9cd3").grid(row=0,column=0)

for count,A in enumerate(sorted(SummativeRubrics)):
  tk.Button(SAButtons, text=A, command=lambda x=A: SARubric(x)).grid(row=count+1, column=0)



"""this will be for the initial announcements"""

AnnDict = {}
AnnDict[210] = {}
AnnDict[210][1] = "zyBook reading on geometry basics and triangles\nReviewQuiz"
AnnDict[210][2] = "zyBook reading on polygons, perimeter, and area\nReviewQuiz"
AnnDict[210][3] = "zyBook reading on geometry basics and triangles\nReview Quiz\nSummative Assessment: HOA Building Request"
AnnDict[210][4] = "zyBook reading on analytic geometry and trigonometry\nReview Quiz\nSummativeAssessment: Arranging Furniture"
AnnDict[210][5] = "zyBook reading on non-Euclidean geometries\nReview Quiz\nSummative Assessment: Non-Euclidean Geometries"

AnnDict[217] = {}
AnnDict[217][1] = "zyBook reading on introductions to statistical investigations and significance\nReviewQuiz"
AnnDict[217][2] = "zyBook reading on generalization\nReviewQuiz\nSummative Assessment: Sampling Research Article"
AnnDict[217][3] = "zyBook reading on estimation and causation\nReview Quiz\nSummative Assessment: Confidence Intervals"
AnnDict[217][4] = "zyBook reading on comparing two proportions\nReview Quiz"
AnnDict[217][5] = "zyBook reading on comparing two means\nReview Quiz\nSummative Assessment: Statistical Methods Research Article"


AnnDict[221] = {}
AnnDict[221][1] = "zyBook reading on logic, proof, and sets\nWk1 Summative Assessment"
AnnDict[221][2] = "zyBook reading on functions, Boolean algebra, and logic gates"
AnnDict[221][3] = "zyBook reading on integer properties and counting\nWk3 Summative Assessment"
AnnDict[221][4] = "zyBook reading on computation and induction with recursion"
AnnDict[221][5] = "zyBook reading on discrete probability, graphs, and trees\nWk5 Summative Assessment"

tk.Label(Announcements, text="First, navigate to the announcements page of the course.  Next, choose which course the announcements are for.  Finally, type the date of the first Thursday for the course in the form MM/DD/YY.", bg="green").pack(pady=10)

CN = ttk.Combobox(Announcements, values=["210", "217", "221"])
CN["state"] = "readonly"
CN.pack(pady=10)
CN.set("210")

FirstThursday = tk.Text(Announcements, height=1, width=10)
FirstThursday.pack(pady=10)
FirstThursday.insert("1.0", "MM/DD/YY")

tk.Button(Announcements, text="Enter", command=PostAnnouncements,width=20, bg="#444", fg="white").pack(pady=20)

ttk.Separator(root, orient="horizontal").pack(fill="x")

tk.Label(Announcements,text="To create an announcement for published grades, nagivate to the announcements page and choose the week these grades are for.", bg="green").pack(pady=10)

WW = ttk.Combobox(Announcements, values=["1", "2", "3", "4", "5"])
WW["state"] = "readonly"
WW.pack(pady=10)
WW.set("1")

tk.Button(Announcements, text="Enter", command=ScoresPublishedAnnouncement,width=20, bg="#444", fg="white").pack(pady=20)


"""
CourseNumber = 210 #MTH/CourseNumber
FT = datetime.datetime.strptime("11/21/24","%m/%d/%y") #FT stands for "FirstThursday"
"""





# Show the main screen initially
show_frame(main_screen)

# Start the Tkinter event loop
root.mainloop()
