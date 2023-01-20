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
        accessKeyId: 'ASIAUGNLVVIW2FP23ONZ',
        secretAccessKey: 'Il6lIljA/eaqUizFl4Mj2tFG/sNkEZ/8nffET3NA',
        sessionToken:'FwoGZXIvYXdzEDIaDEXQyD0hTavEPNifVCK9AflgcBdUo6/OGqeiiVkbElBTQNPCru4kj2rreAulFdc/Pvdyj6pY4GiPQjNyfShw6RYv5mKNqcYft5Q93iJeua9F5+2cu8Os+r/SNyHGaI0f9N5F7FrMFWuY/WSC9AipLpmJ1Hco1KMSxgiimjl2kFfKOcrBNGwDXHYTJl5i42nUHqFGdGSMScoJtNUWkn2w93h775HITpYjkGRp5M5eJU4AtYLMzVpSf1rPYTbGjvGbFqnGp7E87uhD50FUXyi8pameBjItDXSPA+oVU8FyKZkkH6716p5iysQEEW+gPDl1yAoO8Tl6rBCALvqR43SfmDpE',
        region: 'us-east-1'
      }
}