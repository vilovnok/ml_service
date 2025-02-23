import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-custom-paginator',
  templateUrl: './custom-paginator.component.html',
  styleUrls: ['./custom-paginator.component.scss']
})
export class CustomPaginatorComponent implements OnInit {
  
  @Input() totalItems: any;
  @Input() currentPage: any;
  @Input() itemsPerPage: any;
  
  totalPages = 0;
  pages:number[]=[];
  constructor() {}
  
  ngOnInit(): void {
    if(this.totalItems){
    this.totalPages=Math.ceil(this.totalItems / this.itemsPerPage);
    this.pages=Array.from({length: this.totalPages}, (_, i)=> i + 1);
   }
  }



}
