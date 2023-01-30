export interface User {
    username: string;
    password: string;
}

export interface Credential {
    accessKeyId: string,
    secretAccessKey: string,
    sessionToken:string,
    region: string
  }

export class GlobalVar{
    public static connectedUser:User={username:"",password:""}
    public static credentials:Credential={
        accessKeyId: 'ASIAUGNLVVIWRXDI66O2',
        secretAccessKey: '7za6/XEUAoYbzfcZL0D0R9sexZWCTFMV7BIoLXpm',
        sessionToken:'FwoGZXIvYXdzECYaDAZDKiSHX6mDFGyB4iK9Af0p3xkbjBRMnKHcks+wfNRQyO7O0wYHts1JI6vNC5ZGQLNnv/JNJkPWZRbN8S8/ofKNQCGW3bufDjXivmi9osypGYZ/QSUQBlxejOw7UWk3lvxVltsGltUx9BZTqtmzgl8rCGtCmmvUQBKCG55lJfI+SIoAxX8iUxzoeCALbFD1CiJljVCMoGwFuLy221jtJcVce1eWpz6qZ1FiHeHJPJt8LMQDGBt0kqEs7oDiBwPgu4fP9Rq9jHsi6pMneSiJ+d6eBjItuO+Hcp+4Pv+QzsLg0eIOZrxBp2Vx5KEYE4WQhimR6WtyQrZ/GK8HU6yIjSjA',
        region: 'us-east-1'
      }
}