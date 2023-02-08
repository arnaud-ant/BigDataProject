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
        accessKeyId: 'ASIARQRVCA2QZZFJL4VW',
        secretAccessKey: 'jIXiBihPUJwxd3/e4MmDj7SR8E6awfoxLFRGDN9N',
        sessionToken:'FwoGZXIvYXdzEP///////////wEaDCJutqEn34AY+D/OXiK9AXkHn4/nOv9vFuAL3ClBoucY5oCJCXgs0rFEnEZVVzZ3v77+9so8Fn0mozaWDedjPpmSGIMgXjo1TmbDC2d8ZoG1crn8bsvCz6Zs6+PzEe7S0Mbvy4upGW/FEO2EJl0UrMVJEzqZEsfldvp+YaMne4MKtrio4rz24y7P3czxVFH5Z+38FtXL2BUDpofQL80hUqHEHMJy6qT5igdfK3Z7hHbZbpi9wCLGrbdVBfqXjrp3mxUGUvRsC4DPepF5QijyvY6fBjItBXEFO89U9hTC1PZmBdjqbwTxTEeIF1Nfq/mNsV9NYSup2MLHARhUepXsNJkf',
        region: 'us-east-1'
      }
}