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
        accessKeyId: 'ASIAUGNLVVIW73YRXPWH',
        secretAccessKey: 'HhW6nJiLNwJBUM6fRSDszhVlvm7IJE1aXN0XyWUP',
        sessionToken:'FwoGZXIvYXdzECMaDCkXdvPdu+69c+sbFSK9AZKhtRijPV92Rv5Krty3HVW7H3nDsJSU1Y4lver+ZuutRaZKcePYSI9ZxO3vy0ojYdmqDkAoyEtNw8nqRPN7ueRNcdZqIpRnsP5CDdWelGcptZ3XdbFJBbuN/41/GI2igxA0+CyED5+TrTEzuKgvPvFNFp7wG7lQ+v/Ut04PRxKihaBD9Wn4khxDcTbELVd+qOOC1vEuYk9WmLwuNIxn3mEAfP1FOBJMYeSsGu8zv0ZEe24mu/+JlL1K8T+kqii496WeBjItQFcAWXzthuG++EjhJ8MlBC1kKIn7JbIJt3DJinjLAnN0thQQn2vDVWiYbmuZ',
        region: 'us-east-1'
      }
}