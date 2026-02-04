export type Priority = 'Low' | 'Medium' | 'High';

export type Task = {
  id: number;
  title: string;
  deadline: string;
  priority: Priority;
  comments: string;
  completed: boolean;
};
