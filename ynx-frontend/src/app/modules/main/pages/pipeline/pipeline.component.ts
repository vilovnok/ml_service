import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { FormBuilder } from '@angular/forms';
import { NgToastService } from 'ng-angular-popup';

import { PageEvent } from '@angular/material/paginator';
import { LoadingHandler } from 'src/app/helpers/loading-handler';
import { MatDialog } from '@angular/material/dialog';
import { PopupFilterComponent } from '../../components/popup-filter/popup-filter.component';


@Component({
  selector: 'app-pipeline',
  templateUrl: './pipeline.component.html',
  styleUrls: ['./pipeline.component.scss']
})
export class PipelineComponent implements OnInit {

  public pipes: any = [];

  display_btn_h: boolean = false;
  currentPage = 1;
  totalPages = 0;
  itemsPerPage = 10;
  loadingHandler = new LoadingHandler();
  pages: number[] = [];
  searchText: string = '';

  onSearchTextEntered(searchValue: string) {
    this.searchText = searchValue;
  }

  constructor(
    private fb: FormBuilder,
    private service: AuthService,
    private toast: NgToastService,
    private dialog: MatDialog) {}

  ngOnInit(): void {this.loadpipes();}
  loadpipes() {
    this.loadingHandler.showLoading();
    this.service.handle_get_all_requests('pipe/pipes').subscribe(result => {
      let totalItems = result.pipes.length;
      if (totalItems > 0) {
        this.display_btn_h = true;
        this.pipes = result.pipes;
        this.loadingHandler.hidenLoading();
        this.Paginator(totalItems);
        this.sortPipesByTimeDesc(this.pipes);
        this.loadingHandler.hidenLoading();
      } else {
        this.toast.warning({ detail: "Attention", summary: "No files have been sent yet", duration: 5000 });
        this.loadingHandler.hidenLoading();
      }
    });
  }

  sortPipesByTimeDesc(pipes: any) {
    this.pipes.forEach((pipe: any) => {
      pipe.duration_time = new Date(pipe.duration_time).toString().split('GMT')[0].trim();
    });
    this.pipes.sort((a: any, b: any) => {
      const timeA = new Date(a.duration_time).getTime();
      const timeB = new Date(b.duration_time).getTime();
      return timeB - timeA;
    });
  }

  download_file(task_id: string, file_name: string, status: string) {
    if (status == 'success') {
      this.service.DownloadFile(task_id).subscribe(res => {
        let blob: Blob = res.body as Blob;
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = file_name;
        a.click();
      }, (err) => {
        // console.log(`Error: ${err}`)
      });
    } else if (status == 'pending') {
      this.toast.warning({ 
        detail: "Attention", 
        summary: 'The file is still being processed', 
        duration: 5000 });
    } else {
      this.toast.warning({
        detail: "Attention",
        summary: 'Problems with file processing',
        duration: 5000,

      });
    }
  }

  handlePageEvent(pageEvent: PageEvent) {
    console.log("pageEvent", pageEvent);
    this.currentPage = pageEvent.pageIndex;
  }

  Paginator(totalItems: number) {
    if (totalItems) {
      this.totalPages = Math.ceil(totalItems / this.itemsPerPage);
      // console.log(this.totalPages);
      this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
    }
  }

  navigateToFirstPage() {
    this.currentPage = 1;
  }

  navigateBackward() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  navigateForward() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  navigateToLastPage() {
    this.currentPage = this.totalPages;
  }

  get paginatedData() {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    return this.pipes.slice(start, end);
  }

  show_message() {
    this.toast.warning({ detail: "Attention", summary: "By clicking on the file name, you can download it", duration: 5000 });
  }
  add_filter() {
    this.OpenpopupFilter(12, 'test.txt');
  }

  OpenpopupFilter(task_id: any, file_name: any) {
    var _popup = this.dialog.open(PopupFilterComponent, {
      enterAnimationDuration: '500ms',
      exitAnimationDuration: '500ms',
      data: { task_id: task_id, file_name: file_name }
    });
    _popup.afterClosed().subscribe(item => {});
  }
}