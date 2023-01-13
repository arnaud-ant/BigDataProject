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
        accessKeyId: 'ASIAUGNLVVIW42GSDP4V',
        secretAccessKey: 'XuMncmtsBFW2Mw6TGx1S/l2K2qqT5yJrGQQj6n8I',
        sessionToken:'FwoGZXIvYXdzEIr//////////wEaDNXzihOBl/3rM+Ko3iK9Ab3JpQrTcoRB3g82VTWoSX1xcAsOpAaNHQdL7f5TJGGlFDn9sUpE3zuMSk8mVLL5lCDfzOIzWT1qRMGqORlm2hJgahlZEbS+8HGqpT+ih1RAYtTm8QXt4m+ZvM5rfBssfPgSNwqv/57beaoBwJmU/4EhjQ4yUGq2d4QjbR6uDYHU88bC2VHxIL+f61PNrmCt18U3qn3zbyIYARR1+L9izbgCbVafNJEnBfDWI0dQcayTdUGQGkus0DC5RhSn3Si3u4SeBjItI506SPvq9kYr2u6zoJhq5iIW5EyrqwG+QqwvXBlMusnQbhstSOxYljRbgCvy',
        region: 'us-east-1'
      }
}