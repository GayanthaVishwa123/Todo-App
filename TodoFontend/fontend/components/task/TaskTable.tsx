import React from 'react';
import { Task } from '@/types/task';

type TaskTableProps = {
  title: string;
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  onComplete: (id: number) => void;
  onUndo: (id: number) => void;
};

const TaskTable: React.FC<TaskTableProps> = ({
  title,
  tasks,
  onEdit,
  onDelete,
  onComplete,
  onUndo,
}) => {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      <table className="w-full table-auto border-collapse">
        <thead>
          <tr>
            <th className="px-4 py-2 border-b">Title</th>
            <th className="px-4 py-2 border-b">Deadline</th>
            <th className="px-4 py-2 border-b">Priority</th>
            <th className="px-4 py-2 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id} className={task.completed ? 'bg-gray-100' : ''}>
              <td className="px-4 py-2">{task.title}</td>
              <td className="px-4 py-2">{task.deadline}</td>
              <td className="px-4 py-2">{task.priority}</td>
              <td className="px-4 py-2">
                <button
                  onClick={() => onEdit(task)}
                  className="text-blue-500 mr-2"
                >
                  Edit
                </button>
                <button
                  onClick={() => onDelete(task.id)}
                  className="text-red-500 mr-2"
                >
                  Delete
                </button>
                {task.completed ? (
                  <button
                    onClick={() => onUndo(task.id)}
                    className="text-yellow-500"
                  >
                    Undo
                  </button>
                ) : (
                  <button
                    onClick={() => onComplete(task.id)}
                    className="text-green-500"
                  >
                    Complete
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TaskTable;

