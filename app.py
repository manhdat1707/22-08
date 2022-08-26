
from config import *
# from producer import send_data




@app.route('/login', methods=['POST'])
def login():
    acc = db.account
    name = request.json['name']
    password = request.json['password']
    login_user = acc.find_one({"name":name})
    if login_user:
        if bcrypt.hashpw((password.encode('utf-8')),login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):  
            session['name'] = request.form['name']
            return  'You are logged in as ' + session['name']

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        today = datetime.today()
        acc = db.account
        name = request.json['name']
        password = request.json['password']
        existing_user = acc.find_one({'name' : name})

        if existing_user is None:
            hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            acc.insert_one({'name' : name, 'password' : hashpass,'create_time':today})
            return "wellcome " +name
        
        return 'That username already exists!'
@app.route('/create', methods=['POST'])
def create_user():
    today = datetime.today()
    _name = request.json['name']
    _age = request.json['age']
    _address = request.json['address']
    _phone= request.json['phone']
    _mail = request.json['mail']

    data = db.user.insert_one({
        "name" : _name,
        "age" : _age,
        "address" : _address,
        "phone" : _phone,
        "mail" : _mail,
        "create_time": today,
        "update_time": today
        })
    return jsonify({
        "msg": "user created",
        "id":f"{data.inserted_id}"
    })


@app.route('/user', methods=['GET'])
def get_User():
    results = []
    if r.exists('user'):
        results = json.loads(r.get('user'))
    else :
        data = get_list_user()
        rval = json.dumps(data)
        r.set('user' ,rval)
        results = data
    return jsonify({
        "data": results
    })


@app.route('/account', methods=['GET'])
def get_Account():
    data = get_list_account()
    results = data
    return jsonify ({
        "data": results
    })

@app.route('/del/<id>',methods=['DELETE'])
def del_Account(id):
    del_acc_by_id(id)
    return jsonify({'msg': 'ok'})


@app.route('/update',methods=['POST'])
def update():
    today = datetime.today()
    formatted_datetime = today.isoformat()
    json_datetime = json.dumps(formatted_datetime)
    _name = request.json['name']
    _age = request.json['age']
    _address = request.json['address']
    _phone= request.json['phone']
    _mail = request.json['mail']
    msg = {
        "name" : _name,
        "age" : _age,
        "address" : _address,
        "phone" : _phone,
        "mail" : _mail,
        "update_time": json_datetime
    }
    send_data(msg)
    return jsonify({
            "msg": "data sent to kafka",
            "status": "200"
        })



@app.route('/upload', methods = ["GET", "POST"])
def upload_file():
    user_id = request.form['user_id']
    today = datetime.today()
    formatted_datetime = today.isoformat()
    json_datetime = json.dumps(formatted_datetime)
    if request.method == 'POST':
        f = request.files['avatar']
        cv = request.files['cv']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        cv.save(os.path.join(app.config['UPLOAD_FOLDER'], cv.filename))
        a = db.attachments.insert_one({'cv': cv.filename , 'avatar':f.filename,'create_time':today ,'update_time':today,"user_id":user_id})
        return "file saved"


@app.route('/detail/<id>', methods=['GET'])
def get_User_by_id(id):
    data_user = get_user_by_id(id)
    data_upload = get_attachments_id(id)
    return jsonify ({
        "user": data_user,
        "attachments":data_upload
    })

    
if __name__ == '__main__':
    app.run(debug=True)
