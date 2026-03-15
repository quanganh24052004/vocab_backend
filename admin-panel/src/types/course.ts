export interface Meaning {
  id: string;
  wordId: string;
  vietnamese: string;
  exampleEn?: string;
  exampleVi?: string;
  updatedAt: string;
}

export interface Word {
  id: string;
  lessonId: string;
  english: string;
  phonetic?: string;
  partOfSpeech?: string;
  audioUrl?: string;
  cefr?: string;
  meanings: Meaning[];
  updatedAt: string;
}

export interface Lesson {
  id: string;
  courseId: string;
  name: string;
  subName?: string;
  quantityOfWord: number;
  words: Word[];
  updatedAt: string;
}

export interface Course {
  id: string;
  name: string;
  description: string;
  subDescription?: string;
  lessons: Lesson[];
  updatedAt: string;
  isDeleted: boolean;
}
