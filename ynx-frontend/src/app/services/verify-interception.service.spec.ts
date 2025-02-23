import { TestBed } from '@angular/core/testing';

import { VerifyInterceptionService } from './verify-interception.service';

describe('VerifyInterceptionService', () => {
  let service: VerifyInterceptionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VerifyInterceptionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
