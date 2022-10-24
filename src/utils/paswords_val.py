import bcrypt


class Password:
    def __init__(self, password: str):
        if Password.validation_password(password):
            self.password = password.encode('utf-8')

    def hash_password(self) -> bytes:
        crypt_password = bcrypt.hashpw(self.password, bcrypt.gensalt())
        return crypt_password

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
