# Соре за быдлокод
# Делал в последний момент за пять минут
# Пушто весь день решал CTF, реверсил, ходил на концерт AJR и было совершенно не до этого
# Когда-нибудь я научусь не откладывать вещи на последний час перед делайном
# Но не сегодня :/

import sqlite3
import datetime
import re


conn = sqlite3.connect('pb.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id          INTEGER PRIMARY KEY,
                    name        TEXT,
                    surname     TEXT,
                    birthday   DATE)''')
                    
                    
c.execute('''CREATE TABLE IF NOT EXISTS numbers (
                    id          INTEGER PRIMARY KEY,
                    userid      INTEGER, 
                    type        TEXT,
                    phone     TEXT)''')

ans = 1

def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def print_all_numbers(userid):
  query = "SELECT * FROM numbers WHERE userid = ?"
  c.execute(query, str(userid))
  fa = c.fetchall()
  for idx, ii in enumerate(fa):
      print (str(idx+1)+'. '+str(ii[2])+': '+str(ii[3]))
  print ()
  return fa
def print_records (records):
  if not len(records):
    print("Nothing found")
  else:
    print ()
    for idx, i in enumerate(records):
      birthday = str(i[3])
      if birthday != '0':
        normbd = datetime.datetime(int(birthday[0:4]), int(birthday[5:7]), int(birthday[8:10]))
        bd = normbd.strftime('%d.%m.%Y') + ' ('+str(calculate_age(normbd))+' yo)'
      else:
        bd = 'no info'
      print (str(idx+1)+'.\nName: '+str(i[1])+'\nSurname: '+str(i[2])+'\nBirthday: '+bd+'\nNumbers: ')
      print_all_numbers(str(i[0]))
      print ()

def print_all_records():
  query = "SELECT * FROM users"
  c.execute(query)
  allrecords=c.fetchall()
  print_records(allrecords)
  return allrecords

def validatephone(phone):
  return phone and phone[0]=='8' and len(phone)==11

def validatebirthday(text):
  while True:
        birthday = input(text)
        if not birthday:
          return 0
        else:
          try:
            dd, mm, yy = int(birthday[0:2]), int(birthday[3:5]), int(birthday[6:10])
            return datetime.date(yy, mm, dd)
          except:
            pass

def validatename(text, req=True):
   while True:
        name = input(text)
        if not name and not req:
          return None
        if re.match(r'^[a-zA-Z]+\Z', name):
          return name.lower().title()

def add_number(userid):
  while True:
        phone = input("Enter the number (89991234567): ").replace('+7', '8')
        if validatephone(phone):
          break
  phonetype = input("Enter the number description [mobile]: ")
  if not phonetype:
    phonetype = 'mobile'
  query = "INSERT INTO numbers (userid, type, phone) VALUES (?, ?, ?)"
  c.execute(query, (userid, phonetype, phone))
  conn.commit()

def edit_number(numberid):
  query = "SELECT * FROM numbers WHERE id = ?"
  c.execute(query, numberid)
  numrecord = c.fetchone()
  phone = input("Enter the number ["+str(numrecord[3])+"]: ")
  if not phone:
    phone = numrecord[3]
  phonetype = input("Enter the number description ["+str(numrecord[2])+"]: ")
  if not phonetype:
    phonetype = numrecord[2]
  query = "UPDATE numbers SET type = ?, phone = ? WHERE id = ?"
  c.execute(query, (phonetype, phone, numberid))
  conn.commit()

def delete_number (numberid):
  query = "DELETE FROM numbers WHERE id = ?"
  c.execute(query, numberid)
  conn.comit()

def edit_record(changeid):
  query = "SELECT * FROM users WHERE id = ?"
  c.execute(query, changeid)
  record = c.fetchone()
  name = validatename('Enter new name ['+str(record[1])+']: ', False)
  if not name:
    name = record[1]
  surname = validatename('Enter new surname ['+str(record[2])+']: ', False)
  if not surname:
    surname = record[2]
  birthday = validatebirthday ('Enter new birthday ['+(datetime.datetime(int(str(record[3])[0:4]), int(str(record[3])[5:7]), int(str(record[3])[8:10])).strftime('%d.%m.%Y') if record[3] else 'no info')+']: ')
  if not birthday:
    birthday = record[3]

  query = "UPDATE users SET name = ?, surname = ?, birthday = ? WHERE id = ?"
  c.execute(query, (name, surname, birthday, changeid))
  conn.commit()
  print ("1. Add number")
  print ("2. Change existing number")
  print ("3. Delete existing number")
  print ("4. Nothing")
  try:
    sel = int(input('What do u want: '))
  except:
    sel = 0
  if sel == 1:
    add_number(changeid)
  if sel == 2:
    fa = print_all_numbers(changeid)
    print ("What number do u wanna change? (0 - cancel)")
    try:
      changenum = int(input("id: "))-1
    except:
      changenum=-1
    if (changenum>-1 and changenum<len(fa)):
      edit_number(str(fa[changenum][0]))
  if sel == 3:
    fa = print_all_numbers(changeid)
    print ("What number do u wanna delete? (0 - cancel)")
    try:
      delenum = int(input("id: "))-1
    except:
      delenum = -1
    if (delenum>-1 and delenum<len(fa)):
      delete_number (str(fa[delnum][0]))

def delete_record(delrec):
  query = "DELETE FROM users WHERE id = ?"
  c.execute(query, delrec)
  query = "DELETE FROM numbers WHERE userid = ?"
  c.execute(query, delrec)

def select_record(question, ar = None):
  if not ar:
    ar = print_all_records()
  if not len(ar):
    raise ("No numbers")
  while True:
    print (question)
    try:
      ia = int(input("id: "))-1
    except:
      continue
    if (ia>-1 and ia<len(ar)):
      return str(ar[ia][0])

def is_exists(name, surname):
  query = "SELECT id FROM users WHERE name = ? AND surname = ?"
  c.execute(query, (name, surname))
  fo = c.fetchone()
  if fo:
    return fo[0]
  else:
    return False


while ans:
	 
   print("Please choose the number of the desired operation:\n"
          "1. Add new record to the phonebook\n"
          "2. Edit records\n"
          "3. Delete a record\n"
          "4. Search\n"
          "5. List all records\n"
          "0. Exit")
   try:
    ans = int(input("Answer: "))
   except:
    ans = 6
   
   if ans == 1:
    try:
         name = validatename ("Enter name (Vova): ")
         surname = validatename("Enter surname (Putin): ")
         edid = is_exists(name, surname)
         if edid:
          print (name +' '+surname+'\'s contact already exists. Edit? ')
          if input('y/n? ')=='y':
            edit_record(str(edid))
         else:
           birth = validatebirthday("Enter birthday (14.02.1953)[]: ")
           query = "INSERT INTO users (name, surname, birthday) VALUES (?, ?, ?)"
           c.execute(query, (name, surname, birth))
           query = "SELECT id FROM users WHERE name=? AND surname=?"
           c.execute(query, (name, surname))
           userid = c.fetchone()[0]
           add_number(userid)
           conn.commit()
    except:
      pass

   if ans == 2:
    try:
      edit_record(select_record ("What record do u wanna change?"))
    except:
      print ("Empty phonebook")

   if ans == 3:
    try:
      delete_record(select_record ("What record do u wanna delete?"))
    except:
      print ("Empty phonebook")

   if ans == 4:
    searchparams = dict()
    print ("What do u wanna search (u can left some fields empty)")
    searchparams['name'] = input ("Name []: ")
    searchparams['surname'] = input ("Surname []: ")
    birthday = input ("Birthday (31.06) []: ")
    phone = input ("Phone number []: ")
    query = "SELECT * FROM users WHERE "
    isspempty = True
    for i in searchparams.keys():
      if searchparams[i]:
        isspempty = False
        query += i+" LIKE ? AND "
    if not isspempty:
      query = query[:-4]
    if phone:
      if not isspempty:
        query += "AND id IN (SELECT userid FROM numbers WHERE phone = ?"
      else:
        isspempty = False
        query += "id IN (SELECT userid FROM numbers WHERE phone = ?)"
    if birthday:
      if not isspempty:
        query += "AND strftime('%m-%d', birthday) = '?-?'"
      else:
        isspempty = False
        query+="strftime('%m-%d', birthday) = ?"
    if isspempty:
      print("Nothing to search")
    else:
      queryparams = list()
      for key, i in searchparams.items():
        if i:
          queryparams.append('%'+i+'%')
      if phone:
        queryparams.append(phone)
      if birthday:
        dd, mm = birthday[0:2], birthday[3:5]
        queryparams.append(mm+'-'+dd)
      c.execute(query, queryparams)
      allrecords=c.fetchall()
      print_records(allrecords)
      print (" 1. Edit\n2. Delete\n3. Nothing")
      try:
        anss = int(input("Answer: "))
      except:
        anss = 3
      if anss == 1:
        edit_record(select_record ("What record do u wanna change?", allrecords))
      if anss == 2:
        delete_record(select_record ("What record do u wanna delete?", allrecords))

   if ans == 5:
      print_all_records()




