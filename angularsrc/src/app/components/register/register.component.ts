import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormGroupDirective , Validators } from '@angular/forms';
import { Route, Router } from '@angular/router';
import { CommonService } from 'src/app/common.service';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  register:any = FormGroup;
  id:any=4;
  url: any = 'http://localhost:5000/api/register-user';
  constructor(private fb:FormBuilder,private router:Router,private comServ:CommonService, private http: HttpClient) { }

  ngOnInit(): void {
    this.register=this.fb.group({
      email:['',Validators.compose([Validators.required,Validators.email])],
      password:['',Validators.required]
    })

  }

  registerSubmit(data:any){
    console.log(data);
    let dataToPass = {
      email:data.email,
      password:data.password,
      id:this.id++
    }
    
    // this.comServ.addUser(dataToPass).subscribe((data:any)=>{
    //   console.log(data);
    // });
    this.http.post(this.url,dataToPass).subscribe((data:any)=>{});
    alert("Registerd");
    this.router.navigate(['login']);
  }
  gotToLogin(){
    this.router.navigate(['login']);
  }

}