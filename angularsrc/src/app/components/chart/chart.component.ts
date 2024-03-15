import { HttpClient } from '@angular/common/http';
import { Component, AfterViewInit, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Chart , registerables} from 'chart.js';

@Component({
	selector: 'app-charts',
	templateUrl: './chart.component.html',
	styleUrls: ['./chart.component.scss']
})

export class ChartsComponent implements OnInit {
	
	dataPoints: any = [];
	templist: any = [];
	chart: any;
	dates:any =[];
	salesvalue:any = [];
	forevalue:any = [];
	commentlist: any =[];
	showcomment: boolean = false;
	showchart : boolean = false;
	constructor(private http: HttpClient,private router:Router) { Chart.register(... registerables) }
	ngOnInit(): void {
		let url = "http://localhost:5000/api/get_data"
		this.http.get<any>(url).subscribe((data) => {
			this.templist = data;
			for (let i = 0; i < this.templist['sales'].length; i++) {
				let t1 =this.templist['date'][i]
				let t2 = Number(this.templist['sales'][i])
				let cord = {
					x: t1, y: t2
				}
				this.dates.push(t1);
				this.salesvalue.push(cord);
			}

			for (let i = 0; i < this.templist['forecast'].length; i++) {
				let t1 = this.templist['date'][this.templist['sales'].length + i]
				let t2 = Number(this.templist['forecast'][i])
				let cord = {
					x: t1, y: t2
				}
				this.dates.push(t1);
				this.forevalue.push(cord);
			}
			console.log(this.dates);
			console.log(this.salesvalue);
			console.log(this.forevalue);
			console.log(this.templist['comments'])
			this.commentlist=this.templist['comments'];
		});
	}
	
	getdata() {
		this.showchart = true;
		this.showcomment = false;
		const hello = new Chart('myChart', {
			type: 'line',
			data: {
				labels: this.dates,
				datasets: [{
					label: 'Sales',
					data: this.salesvalue,
					tension: 0.3,
					borderColor: 'rgba(92, 154, 247)',
					backgroundColor: 'rgba(92, 154, 247)'
				},
				{
					label: 'Forecast',
					data: this.forevalue,
					tension: 0.3,
					borderColor: 'rgba(242, 120, 63)',
					backgroundColor: 'rgba(242, 120, 63)'
			}]
			},
			options: {
				scales: {

				}
			}
		});
	}
	
	getcomment(){
		this.showchart = false;
		this.showcomment = true;
	}
	signoutfromchart(){
		this.router.navigate(['login'])
	}
}