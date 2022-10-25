import bcrypt

#encript and validate password
class Password:
    def __init__(self, password: str, validate=False):
        if validate:
            Password.validation_password(password)

        password = password.encode('utf-8')
        self.password = password
        self.hash_password = Password.encrypt_password(password)

    @staticmethod
    def encrypt_password(password) -> bytes:
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, exist_salt_password: bytes | str) -> bool:
        if type(exist_salt_password) == str:
            exist_salt_password = exist_salt_password.encode('utf-8')
        return bcrypt.checkpw(self.password, exist_salt_password)

    @staticmethod
    def validation_password(password: str) -> bool:
        if len(password) < 8:
            raise ValueError('Too short, your password has to be more than 8 char')
        digit_count = 0
        for i in password:
            if i.isdigit():
                digit_count += 1
        if not digit_count > 0:
            raise ValueError('Password must contain at least one number')
        return True
