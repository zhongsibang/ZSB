import jwt
import bcrypt

salt1 = bcrypt.gensalt() #生成盐，随机
print(salt1)
salt2 = bcrypt.gensalt()
print(salt2)

password = b'123456'
print(bcrypt.hashpw(password,salt1))
#生成密文，如果盐相同，同样密码密文相同
# b'$2b$12$83lMz9rwYpsxulFwh8zxQuWcPlzLZVDnlIorkbbj.gv200QD0wRiO'

bcrypt.hashpw(password,bcrypt.gensalt()) #如果盐不同，相同密码密文不同
ret = bcrypt.checkpw(password,b'$2b$12$83lMz9rwYpsxulFwh8zxQuWcPlzLZVDnlIorkbbj.gv200QD0wRiO')
#验证过程，参数是密码和加密后的密文，返回布尔值
print(ret)