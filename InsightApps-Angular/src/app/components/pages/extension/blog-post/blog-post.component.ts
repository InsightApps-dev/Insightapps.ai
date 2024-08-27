import { Component, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Editor, NgxEditorModule, Toolbar, Validators } from 'ngx-editor';
import * as FilePond from 'filepond';
import { FilePondComponent, FilePondModule } from 'ngx-filepond';
import { SharedModule } from '../../../../shared/sharedmodule';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';
import { NgSelectModule } from '@ng-select/ng-select';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-blog-post',
  standalone: true,
  imports: [SharedModule,NgbModule,FilePondModule,CommonModule,NgxEditorModule,FormsModule,ReactiveFormsModule,NgSelectModule,RouterModule],
  templateUrl: './blog-post.component.html',
  styleUrls: ['./blog-post.component.scss']
})
export class BlogPostComponent {
  constructor() {
    this.editor = new Editor();
  }

  editor!: Editor;
  toolbar: Toolbar = [
    ['bold', 'italic'],
    ['underline', 'strike'],
    ['code', 'blockquote'],
    ['ordered_list', 'bullet_list'],
    [{ heading: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] }],
    ['link', 'image'],
    ['text_color', 'background_color'],
    ['align_left', 'align_center', 'align_right', 'align_justify'],
  ];
  ngOnInit(): void {
  }
  public onUploadInit(args: any): void {
    console.log('onUploadInit:', args);
  }
  
  public onUploadError(args: any): void {
    console.log('onUploadError:', args);
  }
  
  public onUploadSuccess(args: any): void {
    console.log('onUploadSuccess:', args);
  }
  @ViewChild("myPond") myPond!: FilePondComponent;
  
  pondOptions: FilePond.FilePondOptions = {
    allowMultiple: true,
    labelIdle: "Drop files here to Upload...",
  };
  singlepondOptions: FilePond.FilePondOptions = {
    allowMultiple: false,
    labelIdle: "Drop files here to Upload...",
  };
  
  pondFiles: FilePond.FilePondOptions["files"] = [
   
  ];
  
  pondHandleInit() {
  
  }
  
  pondHandleAddFile(event: any) {
  
  }
  
  pondHandleActivateFile(event: any) {
  
  }
  form:any = new FormGroup({
    editorContent: new FormControl(
      { value: '', disabled: false },
      Validators.required()
    ),
  });
}
