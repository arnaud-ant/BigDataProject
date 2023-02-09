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
        accessKeyId: 'ASIARQRVCA2QURLNPRGI',
        secretAccessKey: 'lh/dRqnC108E8qlMCaDD8RMVs04XO/mj+0jEY1+D',
        sessionToken:'FwoGZXIvYXdzEBsaDKbkmVFLakOBtGekuiK9AblYTlRM3mlHz5rNPvXq0xYAR1z2GILpuJNvD/X1S4xOB1QA/2Z2GjzwcVjtgnJPOmEmW944ALOfQ+uo8Zn4VkLqZUqulCrvDwNCqd6RMkuKjlgw/njnFEPrtIg6oR3pvgS92gYBU+OAZUPgOBLMI58Op0ySRaCmk+6nJOUKUULgBFREf+QRNOXPs78blCdRzabtEUT9hZjrQiJnuoRp100FlCH2WC2qEcctCmwhhEsylKcJOPrV9CGE5dnswCij6pSfBjIttHmtLeM5m21h/gFQnj1MCYHBDiRUVFW4hDj2DZZmsbUpAUqmSsB38jTpnqqE',
        region: 'us-east-1'
      }
}