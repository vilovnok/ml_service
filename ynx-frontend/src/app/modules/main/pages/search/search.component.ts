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
      'text': "Привет! Я MedFusion - твой персональный помощник по доказательной медицине.\n\nОсобенности: \n1) В моей базе данных содержатся только обзоры статей с сайта доказательной медицины Cochrane Library, опубликованные с 2003 года по ноябрь 2024 года. В моей базе данных нет клинических рекомендаций, но я все равно постараюсь тебе помочь! \n2) Я умею отвечать на общие медицинские вопросы, а также искать информацию по конкретной статье (по точному названию или по ссылке на doi). \n3) В нашем диалоге я помню только последние четыре сообщения. Историю чата можно сбросить при нажатии кнопки clear.\n4) По окончании диалога, пожалуйста оставьте обратную связь, нажав на 👍/👎 \n5) Я могу тратить до нескольких минут на ответ, поскольку очень тщательно ищу для вас информацию, прошу прощения за возможное длительное ожидание!",
    },
    {
      'role': 'human',
      'text': "Привет! Я MedFusion - твой персональный помощник по доказательной медицине.\n\nОсобенности: \n1) В моей базе данных содержатся только обзоры статей с сайта доказательной медицины Cochrane Library, опубликованные с 2003 года по ноябрь 2024 года. В моей базе данных нет клинических рекомендаций, но я все равно постараюсь тебе помочь! \n2) Я умею отвечать на общие медицинские вопросы, а также искать информацию по конкретной статье (по точному названию или по ссылке на doi). \n3) В нашем диалоге я помню только последние четыре сообщения. Историю чата можно сбросить при нажатии кнопки clear.\n4) По окончании диалога, пожалуйста оставьте обратную связь, нажав на 👍/👎 \n5) Я могу тратить до нескольких минут на ответ, поскольку очень тщательно ищу для вас информацию, прошу прощения за возможное длительное ожидание!",
    },
    {
      'role': 'ai',
      'text': "Привет! Я MedFusion - твой персональный помощник по доказательной медицине.\n\nОсобенности: \n1) В моей базе данных содержатся только обзоры статей с сайта доказательной медицины Cochrane Library, опубликованные с 2003 года по ноябрь 2024 года. В моей базе данных нет клинических рекомендаций, но я все равно постараюсь тебе помочь! \n2) Я умею отвечать на общие медицинские вопросы, а также искать информацию по конкретной статье (по точному названию или по ссылке на doi). \n3) В нашем диалоге я помню только последние четыре сообщения. Историю чата можно сбросить при нажатии кнопки clear.\n4) По окончании диалога, пожалуйста оставьте обратную связь, нажав на 👍/👎 \n5) Я могу тратить до нескольких минут на ответ, поскольку очень тщательно ищу для вас информацию, прошу прощения за возможное длительное ожидание!",
    },
    {
      'role': 'human',
      'text': "Привет! Я MedFusion - твой персональный помощник по доказательной медицине.\n\nОсобенности: \n1) В моей базе данных содержатся только обзоры статей с сайта доказательной медицины Cochrane Library, опубликованные с 2003 года по ноябрь 2024 года. В моей базе данных нет клинических рекомендаций, но я все равно постараюсь тебе помочь! \n2) Я умею отвечать на общие медицинские вопросы, а также искать информацию по конкретной статье (по точному названию или по ссылке на doi). \n3) В нашем диалоге я помню только последние четыре сообщения. Историю чата можно сбросить при нажатии кнопки clear.\n4) По окончании диалога, пожалуйста оставьте обратную связь, нажав на 👍/👎 \n5) Я могу тратить до нескольких минут на ответ, поскольку очень тщательно ищу для вас информацию, прошу прощения за возможное длительное ожидание!",
    },
  ];

  constructor(
    private service: AuthService,
    private fb: FormBuilder,
    private toast: NgToastService,
    private router: Router,
    private sanitizer: DomSanitizer) { }


  ngOnInit(): void { 
    // this.loadposts(); 
  }


  async generate() {
    if (!this.input_text.trim()) {
      this.input_text = '';
      return;
    }
    if (!localStorage.getItem('token') || localStorage.getItem('token') === undefined) { 
      return;
    }      

    const role = 'human';
    const human_text = this.input_text.trim();
    this.addMessage(role, human_text)
  
    this.input_text = '';
    await this.sleep(2000);
    this.istyping = true;

    const reqBody = {      
      "text": human_text,
      "user_id": localStorage.getItem('user_id')
    }

    this.service.handle_post_requests(reqBody, 'agent/generate').subscribe(async response => {
      
      await this.sleep(1000);
      this.istyping = false;
      const role = response['role']
      const ai_text = response['ai_text'].replace(/Ссылки[\s\S]*/g, '');      
      const metadata = response['full_metadata']
      const id = response['id']
      this.addMessage(role, ai_text, true, metadata, id);
    }, async error => {
      
      await this.sleep(2000);
      const role = 'ai';
      const bot_text = 'Произошла ошибка при обработке вашего запроса. Пожалуйста, проверьте ваш токен.'
      this.addMessage(role, bot_text);
      this.istyping = false;
      this.isPlaye = false;
      localStorage.removeItem('token');
      this.input_text = ''
    });
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

  addMessage(role: string, text: string, 
    isCollapsed?: boolean, 
    collapsibleText?: string, id?: number): void {

  this.messages.push({ 'role': role, 
  'text': text, 
  'isCollapsed': isCollapsed, 
  'collapsibleText': collapsibleText,
  'id': id,
  });

this.scrollToBottom();
}

  getMessage(reqBody: any) {

    interface Message {
      id?: number
      user_id: number;
      ai_text?: string; 
      human_text?: string;
      created_at: string;
      liked?: boolean;
      full_metadata?: string;
  }
    this.service.handle_post_requests(reqBody, 'agent/get-messages').subscribe(response => {
      
      const sortedPosts = response['messages'].posts.sort((a: any, b: any) => {
        return a.id - b.id;
      });

      sortedPosts.forEach((message: Message) => {
        if (message.human_text) {
          this.addMessage('human', message.human_text.trim());
        }
        if (message.ai_text) {
          const ai_text = message.ai_text.replace(/Ссылки[\s\S]*/g, '');
          this.addMessage('ai', ai_text, true, message.full_metadata, message.id);
        }
      });
    }, err => {
      if (err.status === 404){
        this.router.navigate(['reg']);
      }
      
    });
  }






  checkToken(reqBody: any) {
    this.service.handle_post_requests(reqBody, 'agent/check-token').subscribe(response => {
      localStorage.setItem('token', response.token);
      this.isPlaye = true;
    },error => {      
        // this.showDialog('2'); 
        localStorage.removeItem('token');
      this.isPlaye = false;
    });
  }




  loadposts() {
    this.loadingHandler.showLoading();
  }

  
}
