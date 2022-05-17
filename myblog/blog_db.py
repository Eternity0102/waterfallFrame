from waterfall.db.dbConnect import SqlDB

db = SqlDB('localhost',3306,'mydb','root','123456','utf8')
alter_users = db.alter_table('users')
users_table = db.get_fromTable('users')
# users = db.create_table('users')
# users.engine = 'innodb'
# users.set_field({
#     'id':'int',
#     'relname':'varchar(20)',
#     'password':'varchar(20)',
#     'nickname':'varchar(20)',
#     'phone':'varchar(11)',
#     'email':'varchar(20)',
#     'sex':'enum("男","女","保密")',
#     'age':'int',
#     'address':'varchar(50)',
#     'headimg':'varchar(55)',
#     'cookies':'varchar(30),
#     'isActive':'int',
# })
# users.set_primaryKey('id',True)
# users.id = 1
# users.relname = '翔哥'
# users.nickname = '张三'
# users.password = '1234567890'
# users.email= '1234567890@qq.com'
# users.sex = '男'
# users.age = 22
# users.address = '贵州省贵阳市'
# users.create()
# users = db.alter_table('users')
# users.not_null('password')
# users.not_null('nickname')
# users.not_null('phone')
# alter_users.set_autoIncrement('id')
# alter_users.set_unique('nickname')
# alter_users.set_unique('phone')


