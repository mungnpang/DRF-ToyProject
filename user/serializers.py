from rest_framework import serializers

from user.models import User as UserModel


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "phone", "user_type", "join_date"]
        extra_kwargs = {
            'username': {
                'error_messages':{
                    'required':'아이디를 입력해주세요',
                }
            },
            'password':{'write_only':True},
            'email':{
                'error_messages':{
                    'required':'이메일을 입력해주세요',
                    'invalid':'알맞은 형식의 이메일을 입력해주세요',
                }
            },
            'phone':{
                'error_messages':{
                    'required':'전화번호를 입력해주세요',
                }
            },
        }
    
    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    