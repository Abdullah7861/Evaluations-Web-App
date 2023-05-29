from flask import request,redirect,url_for,render_template,session,make_response,flash,Flask
from models import app,db,Images,User,Eval_Count,Evaluations
import base64,csv,zipfile,os,shutil
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
app.config['UPLOAD_FOLDER'] = 'ImagesFolder'



def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function






@app.route("/logout")
@login_required
def logout():
    session.clear()
    print(session)
    return redirect(url_for("login"))

@app.route("/",methods = ["GET","POST"])
def login():
    if session.get('logged_in'):
        redirect(url_for("home"))
    if request.method == "POST":
        print("This is triggered")
    #get user credential from form
        name = request.form["uname"]
        password = request.form["psw"]
    #match from database
        if( name == "adminissuper" and password == "password"):
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        user = User.query.filter_by(username = name).first()
        if not user:
            return render_template("login.html")
        if password == user.password:
            session["logged_in"] = True
            session["username"] = name
            session["user_id"] = user.id
            return render_template("home.html")
    return render_template("login.html")


@app.route('/edit_user', methods=['POST'])
@admin_login_required
def edit_user():
    user_id = request.form.get('user_id')
    new_username = request.form.get('username')
    new_password = request.form.get('password')

    # Query the user from the database
    user = User.query.get(user_id)

    if user:
        
        try:
        # Update the user's information
            user.username = new_username
            user.password = new_password

        # Commit the changes to the database
            db.session.commit()
            flash('User information updated successfully.', 'success')
        except:
            return "Name Already Exists"
    else:
        flash('User not found.', 'error')

    return redirect('/admin')


@app.route("/admin")
@admin_login_required
def admin():
    return render_template("admin.html")



@app.route("/profile")
@login_required
def profile():
    #get user name
    data = session["username"]
    #get user credentials from the database
    
    #render the profile template with the extracted data from the database
    return render_template("profile.html")

@app.route("/home")
@login_required
def home():
        return render_template("home.html")

@app.route('/admin/users')
@admin_login_required
def user_list():
    users = User.query.all()  # Fetch all users from the database

    return render_template('users.html', users=users)


@app.route('/post_previous_evaluations',methods=["POST"])
@login_required
def post_previous_evaluation():
            Critertia1 = request.form["criteria1"]
            Critertia2 = request.form["criteria2"]
            Critertia3 = request.form["criteria3"]
            Critertia4 = request.form["criteria4"]
            Critertia5 = request.form["criteria5"]
            Critertia6 = request.form["criteria6"]
            Critertia7 = request.form["criteria7"]
            Critertia8 = request.form["criteria8"]
            Critertia9 = request.form["criteria9"]
            Critertia10 = request.form["criteria10"]
            img_id = session.get("previous_img_id") + 1
            current_user_id = session["user_id"]
            evaluation = Evaluations.query.filter_by(image_id = img_id,user_id = current_user_id).first()
            evaluation.criteria_1 = Critertia1
            evaluation.criteria_2 = Critertia2
            evaluation.criteria_3 = Critertia3
            evaluation.criteria_4 = Critertia4
            evaluation.criteria_5 = Critertia5
            evaluation.criteria_6 = Critertia6
            evaluation.criteria_7 = Critertia7
            evaluation.criteria_8 = Critertia8
            evaluation.criteria_9 = Critertia9
            evaluation.criteria_10 = Critertia10
            print(evaluation)

            db.session.commit()
            return redirect(url_for("evaluations"))




@app.route("/previous_evaluation")
@login_required
def edit_evaluations():
        current_user_id = session["user_id"]
        ImageId = session["previous_img_id"]
        if ImageId < 1:
             return "No Image Remaining"
        else:
            eval = Eval_Count.query.filter_by(user_id = current_user_id).first()
            total_evals = eval.total_Evals
            image = Images.query.filter_by(id=(ImageId)).first()
            evaluation_list = Evaluations.query.filter_by(image_id=ImageId,user_id = current_user_id).first()
        # Decode the base64-encoded image data
            if not image:
                return render_template("Evaluations.html")
            
            image_binary = base64.b64decode(image.first_image)
            image_binary2 = base64.b64decode(image.second_image)

        # Convert binary data to data URI for use in HTML template
            image_data_uri = 'data:image/jpeg;base64,' + base64.b64encode(image_binary).decode('utf-8')
            image_data_uri2 = 'data:image/jpeg;base64,' + base64.b64encode(image_binary2).decode('utf-8')

            session["previous_img_id"] -=1
            return render_template('EditEvaluations.html',image1 = image_data_uri,image2=image_data_uri2
                                ,Username=session["username"],Evaluations=total_evals,list = evaluation_list)








@app.route("/evaluations")
@login_required
def evaluations():
        current_user_id = session["user_id"]
        user_evals = Eval_Count.query.filter_by(user_id = current_user_id).first()
        total_evals = user_evals.total_Evals
        last_img_evaluated = user_evals.last_img_id
        current_img_id = last_img_evaluated+1
        session["current_img_id"] = current_img_id
        session["previous_img_id"] = last_img_evaluated
        image = Images.query.filter_by(id=(current_img_id)).first()
    # Decode the base64-encoded image data
        if not image:
            return render_template("Evaluations.html")
        image_binary = base64.b64decode(image.first_image)
        image_binary2 = base64.b64decode(image.second_image)


    # Convert binary data to data URI for use in HTML template
        image_data_uri = 'data:image/jpeg;base64,' + base64.b64encode(image_binary).decode('utf-8')
        image_data_uri2 = 'data:image/jpeg;base64,' + base64.b64encode(image_binary2).decode('utf-8')

        return render_template('Evaluations.html',image1 = image_data_uri,image2=image_data_uri2
                               ,Username=session["username"],Evaluations=total_evals)



@app.route('/post_evaluations',methods=["POST"])
@login_required
def get_evaluation():
            Critertia1 = request.form["criteria1"]
            Critertia2 = request.form["criteria2"]
            Critertia3 = request.form["criteria3"]
            Critertia4 = request.form["criteria4"]
            Critertia5 = request.form["criteria5"]
            Critertia6 = request.form["criteria6"]
            Critertia7 = request.form["criteria7"]
            Critertia8 = request.form["criteria8"]
            Critertia9 = request.form["criteria9"]
            Critertia10 = request.form["criteria10"]
            img_id = session["current_img_id"]
            current_user_id = session["user_id"]
            evaluation = Evaluations(image_id = img_id,user_id = current_user_id,
                                        criteria_1=Critertia1,criteria_2=Critertia2,criteria_3=Critertia3
                                        ,criteria_4=Critertia4,criteria_5=Critertia5,criteria_6=Critertia6
                                        ,criteria_7=Critertia7,criteria_8=Critertia8,criteria_9=Critertia9
                                        ,criteria_10=Critertia10)
            db.session.add(evaluation)
            current_eval_count = Eval_Count.query.filter_by(user_id=current_user_id).first()
            current_eval_count.last_img_id = img_id
            current_eval_count.total_Evals +=1

            db.session.commit()
            return redirect(url_for("evaluations"))


from flask import send_file

@app.route("/admin/download_evaluations")
@admin_login_required
def download_evaluations():
    if session.get("admin_logged_in"):
        evaluations = Evaluations.query.all()

        # Create a CSV string from the evaluations data
        csv_data = []
        for evaluation in evaluations:
            csv_data.append([
                evaluation.image_id,
                evaluation.user_id,
                evaluation.criteria_1,
                evaluation.criteria_2,
                evaluation.criteria_3,
                evaluation.criteria_4,
                evaluation.criteria_5,
                evaluation.criteria_6,
                evaluation.criteria_7,
                evaluation.criteria_8,
                evaluation.criteria_9,
                evaluation.criteria_10
            ])

        # Create a temporary file to store the CSV data
        temp_csv_file = "evaluations.csv"
        with open(temp_csv_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Image ID", "User ID", "Criteria 1", "Criteria 2", "Criteria 3", "Criteria 4",
                             "Criteria 5", "Criteria 6", "Criteria 7", "Criteria 8", "Criteria 9", "Criteria 10"])
            writer.writerows(csv_data)

        # Send the file in the response
        return send_file(temp_csv_file, as_attachment=True)
    else:
        return "NOT ALLOWED"


@app.route('/delete_user', methods=['POST'])
@admin_login_required
def delete_user():
    user_id = request.form.get('user_id')

    # Perform the deletion logic here
    # For example, you can use SQLAlchemy to delete the user from the database
    # Assuming you have a Users model defined
    evals = Eval_Count.query.get(user_id)
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.delete(evals)
        db.session.commit()
        return redirect(url_for("user_list"))  # Redirect to the admin page after successful deletion
    else:
        return 'User not found.'



@app.route('/admin/create_user', methods=['POST'])
@admin_login_required
def create_user():
    Username = request.form.get('username')
    password = request.form.get('password')

    # Create a new User instance
    existingName = User.query.filter_by(username = Username).first()

    if(existingName):
        return "User already exists"
    else:
         new_user = User(username=Username, password=password)
         eval = Eval_Count(total_Evals = 0,last_img_id = 0)
         db.session.add(new_user)
         db.session.add(eval)
         db.session.commit()
    # Add the new user to the database
    

    flash('New user created successfully.', 'success')
    return redirect('/admin')



@app.route('/upload_zip', methods=['POST'])
@admin_login_required
def upload_zip():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded'

    file = request.files['file']

    # Check if the file has a zip extension
    if not file.filename.endswith('.zip'):
        return 'Invalid file format. Please upload a zip file'
    if file:
         print("File is uploaded")
    # Extract images from the zip file
    print(file)
    with zipfile.ZipFile(file) as zip_ref:
        # Extract images from the ImageGrad folder
        grad_folder = zip_ref.extractall('Images')
        
        # Extract images from the ImageSolid folder
    
    count = 0

    # Loop through the extracted files in the folders
    for filename1 in os.listdir('.\Images\ImageGrad'):
        if filename1.endswith('~'):  # skip temporary files created by some text editors
            continue
        for filename2 in os.listdir('.\Images\ImageSolid'):
            if filename2.endswith('~'):
                continue
            if filename1[:-5] == filename2[:-5]:  # check for matching filenames except for the last character
                print("Condition true")
                file1_id = filename1.split("_")[0]
                file2_id = filename2.split("_")[0]
                try:
                    print(add_image(file1_id, ".\Images\ImageGrad\\" + filename1, ".\Images\ImageSolid\\" + filename2))
                    count += 1
                except:
                     return "Key Error"
    print(f'{count}'"Imagees added")
    shutil.rmtree("Images")
    return redirect("admin")


def add_image(Id, Image1path, Image2path):
    with open(Image1path, 'rb') as f:
        image1_binary = f.read()

    with open(Image2path, 'rb') as f:
        image2_binary = f.read()

    # Encode binary data as base64 string
    image1_data = base64.b64encode(image1_binary).decode('utf-8')
    image2_data = base64.b64encode(image2_binary).decode('utf-8')

    with app.app_context():
        new_image = Images(id=Id, first_image=image1_data, second_image=image2_data)
        db.session.add(new_image)
        db.session.commit()

    return 'Images added to database'





if __name__=="__main__":
    app.secret_key = "ThisisaSupersecretkey4y85y84"
    app.run(debug=True)
