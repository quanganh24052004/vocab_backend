import axiosInstance from './axios';

export const courseApi = {
  getCourses: (skip = 0, limit = 100) => 
    axiosInstance.get(`/courses/?skip=${skip}&limit=${limit}`),
  
  getCourseDetail: (id: string) => 
    axiosInstance.get(`/courses/${id}`),
  
  createCourse: (data: any) => 
    axiosInstance.post('/courses/', data),
  
  updateCourse: (id: string, data: any) => 
    axiosInstance.put(`/courses/${id}`, data),
  
  addLesson: (courseId: string, data: any) => 
    axiosInstance.post(`/courses/${courseId}/lessons`, data),
  
  importCourses: (data: any[]) => 
    axiosInstance.post('/courses/import', data),
};

export default courseApi;
