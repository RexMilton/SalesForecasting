import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonService } from 'src/app/common.service';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  login:any = FormGroup;
  users:any = [];
  url :any = "http://localhost:5000/api/read-users";
  url1 :any = "http://localhost:5000/api/register-user";
  constructor(private fb: FormBuilder, private router: Router, private commenserv: CommonService, private http: HttpClient) { }


  ngOnInit(): void {
    this.login = this.fb.group({
      email:['',Validators.compose([Validators.required,Validators.email])],
      password:['',Validators.required]
    })
    // this.commenserv.getUser().subscribe((data:any)=>{
    //   this.users = data;
    // })
    this.http.get<any>(this.url).subscribe((data: any) => {
      this.users = data['data'];
      console.log(this.users);
    });
    console.log(this.users);
  }
  loginSubmit(data: any){
     console.log(data);
     if(data.email){
      this.users.forEach((item:any) => {
        if(item.email === data.email && item.password === data.password){
          console.log("true");
          this.router.navigate(['home']);
        }
        else{
          localStorage.clear();
        }
      });
    }
  }
  gotToSignup(){
    this.router.navigate(['register']);
  }
}
