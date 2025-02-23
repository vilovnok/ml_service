import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PopupFilterComponent } from './popup-filter.component';

describe('PopupFilterComponent', () => {
  let component: PopupFilterComponent;
  let fixture: ComponentFixture<PopupFilterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PopupFilterComponent]
    });
    fixture = TestBed.createComponent(PopupFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
