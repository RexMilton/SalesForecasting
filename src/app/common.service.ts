import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
@Injectable({
  providedIn: 'root'
})
export class CommonService {
  readURL:any = environment.url;
  registerURL : any = environment.url1;
  constructor(private http: HttpClient) { }

  getUser(){
    return this.http.get(this.readURL);
  }
  
  addUser(data:any){
    return this.http.post(this.registerURL,data);
  }
}
