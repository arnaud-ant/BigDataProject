
export var totalScore : any[] = []

export interface User {
    id:number,
    username: string,
    password: string,
}

export interface Credential {
    accessKeyId: string,
    secretAccessKey: string,
    sessionToken:string,
    region: string
  }

export class GlobalVar{
    public static connectedUser:User={id:0,username:"",password:""}
    public static credentials:Credential={
        accessKeyId: 'ASIARQRVCA2Q22HQLRLR',
        secretAccessKey: 'OayK/ZjJSMDvRQLq0EPM7/KXurnfuxEdlSNjO0uq',
        sessionToken:'FwoGZXIvYXdzEBMaDJJqzhTus2g+6ey/jSK9AW513mg9Mld1WIncmj3+y7HI/Xc20eZXxjtMY2xW77oIA+1vtBwjSykpil3ddSjTjhfsHnO+8IK7HwZUr+lvo+AWXoIosbGx67hEQL5ToMvuV0dTHsqShOuiUtbq0LRFbnSNQivbj2AODcMXYZV2eOqOzf/MXLy+7xHRid1wmEDFa9OjafFP8lmT0qOUBwedTUrnT6MeNAhbJyah163fm/U6Pq7KajEC3Hp5+QKZMZIZCN8gUeiL+tql8Z/EICjM8ZKfBjItcNulcWO4Y2P53OcnCY+sEHC4YpMWO4QRoHo4SBRBVjV6P6OynM/nEbxY44cb',
        region: 'us-east-1'
      }
}