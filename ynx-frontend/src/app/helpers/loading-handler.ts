import { BehaviorSubject, Observable, of } from "rxjs";
import { delay, switchMap} from "rxjs/operators";

export class LoadingHandler {
    private timeout:any;  
    isLoading = false;

    showLoading() {
        this.timeout = setTimeout(()=>{
            this.isLoading=true;
        }, 1000);
    }
    hidenLoading() {
        this.isLoading=false;
        clearTimeout(this.timeout);
    }
}