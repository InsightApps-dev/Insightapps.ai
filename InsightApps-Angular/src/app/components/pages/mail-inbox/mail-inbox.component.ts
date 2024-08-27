
import { Component, ElementRef, HostListener, Renderer2 } from '@angular/core';
import { FormGroup, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Editor, NgxEditorModule, Toolbar ,Validators} from 'ngx-editor';
import { SharedModule } from '../../../shared/sharedmodule';
import { NgSelectModule } from '@ng-select/ng-select';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-mail-inbox',
  standalone:true,
  imports: [SharedModule, NgbModule, NgxEditorModule, FormsModule, ReactiveFormsModule, NgSelectModule,CommonModule],
  templateUrl: './mail-inbox.component.html',
  styleUrls: ['./mail-inbox.component.scss']
})
export class MailInboxComponent {
  showTotalMails: any;
  i!: boolean;
  constructor(private renderer: Renderer2, private el: ElementRef,public modalService:NgbModal) {}
  showMailNavigation = true;

  toggleMailNavigation() {
    this.showMailNavigation = !this.showMailNavigation;
  }

  toggleTotalMails() {
    this.showTotalMails = !this.showTotalMails;
  }
  closeTotalMails() {
    this.showMailNavigation = true;
  }
  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.handleResize();
  }

 

  handleResize(): void {
    const screenWidth = window.screen.width;

    if (screenWidth > 1399) {
      this.renderer.setStyle(this.el.nativeElement.querySelector('.mails-information'), 'display', 'block');
      this.renderer.removeClass(this.el.nativeElement.querySelector('.total-mails2'), 'd-none');
    } else {
      if (this.i) {
        this.renderer.setStyle(this.el.nativeElement.querySelector('.mails-information'), 'display', 'none');
      }
    }

    // Add other resize logic here...

  }

  onMailTypeClick(): void {
    if (window.screen.width <= 991) {
      this.renderer.setStyle(this.el.nativeElement.querySelector('.total-mails2'), 'display', 'block');
      this.renderer.removeClass(this.el.nativeElement.querySelector('.total-mails2'), 'd-none');
      this.renderer.setStyle(this.el.nativeElement.querySelector('.mail-navigation'), 'display', 'none');
      this.i = true;
    }
  }
  onMailTypeClick1(): void {
    if (window.screen.width <= 991) {
      this.renderer.setStyle(this.el.nativeElement.querySelector('.mail-navigation'), 'display', 'block');
      this.renderer.addClass(this.el.nativeElement.querySelector('.mail-navigation'), 'd-block');
      this.i = true;
    }
  }
  onCloseClick(): void {
    if (window.screen.width < 992) {
      this.renderer.setStyle(this.el.nativeElement.querySelector('.mails-information'), 'display', 'block');
      this.renderer.addClass(this.el.nativeElement.querySelector('.total-mails2'), 'd-none');
      this.i = true;
    }
  }



  OpenEditor(content:any){
    this.modalService.open(content);
  }
 
  ngOnInit(){
    this.editor = new Editor();
  
  }
  public editorContent!: FormGroup;
    editordoc = '';
    public editor!: Editor;
    toolbar: Toolbar = [
      ['bold', 'italic'],
      ['underline', 'strike'],
      ['code', 'blockquote'],
      ['ordered_list', 'bullet_list'],
      [{ heading: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] }],
      ['text_color', 'background_color'],
      ['align_left', 'align_center', 'align_right', 'align_justify'],
    ];
  
    form: any = new FormGroup({
      editorContent: new FormControl(
        { value: `Type Text Here`, disabled: false },
        Validators.required()
      ),
    });

    showNavigation = true;
    showMailsInformation = true; // Adjust the initial state based on your requirements
  
    handleListClick(type: string) {
      // Handle click event for list items
      if (type === 'all') {
        this.showNavigation = false;
        this.showTotalMails = true;
        this.showMailsInformation = false;
      }
      // Add similar logic for other list items
    }
  
    handleUlClick() {
      // Handle click event for UL item
      this.showNavigation = false;
      this.showTotalMails = false;
      this.showMailsInformation = true;
    }
    
}
