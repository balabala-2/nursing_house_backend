

# @router.post('/api/send_auth_code', name='send_auth_code')
# def send_auth_code(tel: User_tel, db: Session = Depends(get_db)):
#     userInfo = managerController.get_user_by_phone_num(db, tel.tel)
#     # code = send_verify_code(tel.tel)
#     # return {"verifycode": code, "userInfo": userInfo.username}
#     return {"verifycode": 123456, "userInfo": userInfo.username}