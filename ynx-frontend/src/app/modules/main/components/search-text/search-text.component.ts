import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-search-text',
  templateUrl: './search-text.component.html',
  styleUrls: ['./search-text.component.scss']
})
export class SearchTextComponent {


  enterSearchValue:string='';

  @Output()
  searchTextChange:EventEmitter<string>=new EventEmitter<string>();


  onSearchTextChange() {
    this.searchTextChange.emit(this.enterSearchValue);
  }

  clearValue() {
    this.enterSearchValue='';
  }

}
