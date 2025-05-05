import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { NgToastService } from 'ng-angular-popup';
import { LoadingHandler } from 'src/app/helpers/loading-handler';
import { AuthService } from 'src/app/services/auth.service';


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  @ViewChild('chatbox') private chatbox!: ElementRef;
  
  istyping: boolean = false;
  isPlaye: boolean = false;
  input_text: string = '';
  loadingHandler = new LoadingHandler();

  public sleep = (ms: number): Promise<void> => { return new Promise((r) => setTimeout(r, ms)); }


  messages: { role: string; text: string; collapsibleText?: string; isCollapsed?: boolean; id?: number  }[] = [
    {
      'role': 'ai',
      'text': 'Привет! Я Yanix - твой персональный помощник. Базируюсь на языковой модели T5 (<a href="https://huggingface.co/r1char9/T5_chat" target="_blank">ссылка</a>).'
    },
  ];

  constructor(
    private service: AuthService,
    private fb: FormBuilder,
    private toast: NgToastService,
    private router: Router,
    private sanitizer: DomSanitizer) { }


  ngOnInit(): void { 
    const reqBody = {'user_id': localStorage.getItem('user_id')}
    this.getMessage(reqBody);
  }


  async generate() {
    const input = this.input_text.trim();
  
    if (!input || !localStorage.getItem('token')) {
      this.input_text = '';
      return;
    }
  
    this.addMessage('human', input);
    this.input_text = '';
    this.istyping = true;
  
    await this.sleep(2000);
  
    const reqBody = { message: input };
    console.log(reqBody);
  
    this.service.handle_post_requests(reqBody, 'generate/generate_text').subscribe(
      async response => {
        const token = response['token'];
  
        const checkInterval = setInterval(() => {
          this.service.handle_get_requests(token, 'generate/get_message').subscribe(
            res => {
              if (res.status === 'completed') {
                clearInterval(checkInterval);
                this.istyping = false;
                this.addMessage('ai', res['message_gen']);
              }
            },
            error => {
              if (error.status !== 404) {
                clearInterval(checkInterval);
                this.istyping = false;
                this.addMessage('ai', 'Произошла ошибка при проверке статуса запроса.');
              }
            }
          );
        }, 2000);
      },
      async error => {
        if (error.status == 403) {
          this.toast.error({
            detail: "Balance",
            summary: error.error.detail,            
          });
          this.istyping = false;
          this.isPlaye = false;
          this.input_text = '';
        }else {
        await this.sleep(2000);
        this.addMessage('ai', 'Произошла ошибка при обработке вашего запроса. Пожалуйста, проверьте ваш токен.');
        this.istyping = false;
        this.isPlaye = false;
        this.input_text = '';
      }}
    );
  }
  

  private scrollToBottom(): void {
    this.chatbox.nativeElement.scrollTop = this.chatbox.nativeElement.scrollHeight;
  }


  sanitizeText(text: string): SafeHtml {
    let formattedText = text.replace(
      /\[([^\]]+)\]\[(https?:\/\/[^\s]+)\]/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return this.sanitizer.bypassSecurityTrustHtml(formattedText);
  }

  addMessage(role: string, text: string, id?: number): void {
  this.messages.push({ 'role': role, 
  'text': text, 
  'id': id,
  });
  this.scrollToBottom();
}

  getMessage(reqBody: any) {
    interface Message {
      id?: number
      user_id: number;
      message_gen?: string; 
      message?: string;
      created_at: string;
  }
    this.service.handle_get_all_requests('generate/get_chat').subscribe(response => {
      const sortedPosts = response['messages'].posts.sort((a: any, b: any) => {
        return a.id - b.id;
      });

      sortedPosts.forEach((message: Message) => {
        if (message.message) {
          this.addMessage('human', message.message.trim());
        }
        if (message.message_gen) {
          const message_gen = message.message_gen.trim();
          this.addMessage('ai', message_gen);
        }
      });
    }, err => {});
  }

  loadposts() {
    this.loadingHandler.showLoading();
  }
}
