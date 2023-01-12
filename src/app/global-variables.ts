export interface User {
    username: string;
    password: string;
  }

export class GlobalVar{
    public connectedUser:User={username:"",password:""}
}