import mysql.connector
from datetime import date, timedelta
current_date = date.today()
new_date = current_date + timedelta(days=30)
new_date_string = new_date.strftime("%Y-%m-%d")
cnx=mysql.connector.connect(user='root',password='Ramana110$',
                            host='127.0.0.1',database='library')
cursor=cnx.cursor()
class student:
    def __init__(self,stu_id):
        self.stu_id=stu_id
    def createdict(self):
        sql3="SELECT*FROM library.student_users"
        cursor.execute(sql3)
        result=cursor.fetchall()
        dict1={}
        field_names = [i[0] for i in cursor.description]
        for i in range(len(result)):
            if result[i][1]==self.stu_id:
                for j in range(len(result[i])):
                    dict1[field_names[j]]={}
                    dict1[field_names[j]]=result[i][j]
                break
            
        for i in dict1:
            print(i,dict1[i])
def homepage():
    global stu_name
    ans=input("New user(Y/n)")
    if ans=='Y':
        create_acc()
    else:
        if login()=="Login Success":
            sql3="SELECT no_book_borrowed FROM library.student_users WHERE student_id=%s"
            cursor.execute(sql3,[stu_id])
            user=cursor.fetchone()
            option=input("UserProfile/Borrow/Return")
            if option=="UserProfile":
                stu_name=student(stu_id)
                stu_name.createdict()
            elif option=="Borrow" and user[0]<4:
                print(f"You can borrow only {4-user[0]} books")
                bk_name1=input("Enter bk name: ")
                sql4="select Book_Name from library.books"
                cursor.execute(sql4)
                user1=cursor.fetchall()
                sql5="SELECT Book_id FROM library.books"
                cursor.execute(sql5)
                user2=cursor.fetchall()
                bks={}
                for i in range(len(user1)):
                    if bk_name1 in user1[i][0]:
                        bks[user2[i][0]]=user1[i][0]
                print(bks)
                bk_name2=input("\nEnter name of book: ")
                bk_id1=next((k for k, bk in bks.items() if bk_name2 == bk), None)
                sql7="SELECT `available/non-available` FROM library.books WHERE Book_id=%s"
                cursor.execute(sql7,[bk_id1])
                status2=cursor.fetchone()
                print(status2[0])
                if status2[0]!='non-available':
                    sql6="UPDATE library.books set `available/non-available`=%s where Book_id=%s"
                    status1="non-available"
                    cursor.execute(sql6,[status1,bk_id1])
                    cnx.commit()
                    sql7="UPDATE library.student_users set `no_book_borrowed`=%s where student_id=%s"
                    upd_bk_borr=user[0]+1
                    cursor.execute(sql7,[upd_bk_borr,stu_id])
                    cnx.commit()
                    sql8="insert into library.borrower_table (date_of_borrowing,borrower_name,borrower_id,due_date,book_id,book_name) values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql8,[current_date,stu_name,stu_id,new_date,bk_id1,bk_name2])
                    cnx.commit()
                    print(f"You had borrowed the book {bk_name2} with id: {bk_id1} successfully on {current_date}")
                else:
                    print(f"The book {bk_name2} with id {bk_id1} is not available")
                homepage()
            elif option=="Borrow" and user[0]==4:
                print("YOU CAN ONLY RETURN")
                homepage()
            elif option=="Return" and 0<user[0]<=4:
                sql9="select book_id,book_name from library.borrower_table where borrower_id=%s"
                cursor.execute(sql9,[stu_id])
                user3=cursor.fetchall()
                print(list(user3))
                en_bk_nm=input("Enter bk_name to be returned: ")
                en_bk_id=int(input("Enter bk id to be returned: "))
                print(en_bk_id,user3[0][0],en_bk_nm,user3[0][1])
                if en_bk_id==user3[0][0] and en_bk_nm==user3[0][1]:
                    sql10=f"select due_date from library.borrower_table where book_id={en_bk_id}"
                    cursor.execute(sql10)
                    user4=cursor.fetchone()
                    print(user4[0],current_date)
                    fn = 0 if (current_date - user4[0]) < timedelta(days=0) else (current_date - user4[0]).days * 1
                    sql11="insert into library.check_out (chk_book_name, ch_book_id, chk_borrower_name, chk_borrower_id, due_date, date_of_return, fine_amount) values(%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql11,[en_bk_nm,en_bk_id,stu_name,stu_id,user4[0],current_date,fn])
                    cnx.commit()
                    sql12=f"update library.books set `available/non-available` ={sta} where Book_id={en_bk_id}"
                    sta="available"
                    cursor.execute(sql12,[sta])
                    cnx.commit()
                    sql13="UPDATE library.student_users set `no_book_borrowed`=%s where student_id=%s"
                    upd_bk_borr=user[0]-1
                    cursor.execute(sql13,[upd_bk_borr,stu_id])
                    cnx.commit()
                    sql14="select fine_amount from library.check_out where chk_boroower_id={user4[0]}"
                    cursor.execute(sql14)
                    res=cursor.fetchone()
                    sql15=f"insert into library.student_users (fine_pending) values ({res[0]})"
                    cursor.execute(sql15)
                    cnx.commit()
                                   
                    
                    print("Successfully added")
                else:
                    print("Fail")
def create_acc():
    try:
        stu_name=input("NAME: ")
        stu_id=int(input("ID: "))
        stu_con_num=int(input("CONTACT NUMBER: "))
        stu_pass=input("Enter pasword: ")
        values=(stu_name,stu_id,stu_pass,stu_con_num)
        sql1="INSERT INTO library.student_users (student_name, student_id, student_contact_number,student_passwordl) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql1,values)
        cnx.commit()
        cursor.execute('SELECT * FROM library.student_users')
        user=cursor.fetchall()
        for i in user:
            if values==i[0:4]:
                print("account created")
                homepage()
    except:
        print('Account failed')
        homepage()
def login():
    global stu_id
    global stu_name
    stu_name=input("NAME:")
    stu_id=int(input("ID:"))
    stu_pass=input("Enter password")
    sql2="SELECT * FROM library.student_users where student_id=%s"
    val=(stu_name,stu_id,stu_pass)
    cursor.execute(sql2,[stu_id])
    user=cursor.fetchall()
    if val == user[0][0:3]:
        return("Login Success")        
    else:
        print("failed")
        homepage()
if __name__=='__main__':
    homepage()
    cnx.close()
