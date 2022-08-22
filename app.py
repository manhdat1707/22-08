
from config import *


@app.route('/login', methods=['POST'])
def login():
    acc = db.account
    name = request.json['name']
    password = request.json['password']
    login_user = acc.find_one({"name":name})
    if login_user:
        if bcrypt.hashpw((password.encode('utf-8')),login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):  
            return "wellcome"

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
            return "wellcome"
        
        return 'That username already exists!'



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

@app.route('/profile',methods=['POST'])
def create_profile():
    today = datetime.today()
    _name = request.json['name']
    _age = request.json['age']
    _address = request.json['address']
    _phone= request.json['phone']
    _mail = request.json['mail']
    db.user.insert_one({
        "name" : _name,
        "age" : _age,
        "address" : _address,
        "phone" : _phone,
        "mail" : _mail,
        "create_time": today
        })

    return jsonify({
        "data":"a"
    })


@app.route('/upload',methods=['POST'])
def upload():
    today = datetime.today()
    avatar = request.json['avatar'],
    cv = request.json['cv']
    result = db.attachments.insert_one({'avatar':avatar,'cv':cv,'create_time': today ,'update_time':{}})
    return jsonify({"data": "a"})
    
if __name__ == '__main__':
    app.run(debug=True)
