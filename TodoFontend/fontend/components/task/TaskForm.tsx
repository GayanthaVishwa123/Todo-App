import { useState, useEffect } from 'react';
import { Task, Priority } from '@/types/task';
import '@/styles/form.css'

type Props = {
  task: Task;
  onSave: (task: Task) => void;
  onClose: () => void;
};

export default function TaskForm({ task, onSave, onClose }: Props) {
  const [title, setTitle] = useState(task.title);
  const [deadline, setDeadline] = useState(task.deadline);
  const [priority, setPriority] = useState<Priority>(task.priority);
  const [comments, setComments] = useState(task.comments);

  // This useEffect is used to update the form when `task` prop changes
  useEffect(() => {
    setTitle(task.title);
    setDeadline(task.deadline);
    setPriority(task.priority);
    setComments(task.comments);
  }, [task]);

  const handleSubmit = () => {
    // Create the updated task object
    const updatedTask: Task = { ...task, title, deadline, priority, comments };
    onSave(updatedTask); 
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-end">
      <div className="w-[420px] bg-white h-full p-6 shadow-xl">
        {/* Heading changes based on whether task has an id or not */}
        <h2 className="text-2xl font-semibold mb-4">{task.id ? 'Edit Task' : 'Create Task'}</h2>

        {/* Title Input */}
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border px-4 py-2 rounded mb-4"
          placeholder="Title"
        />

        {/* Deadline Input */}
        <input
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
          className="w-full border px-4 py-2 rounded mb-4"
        />

        {/* Priority Dropdown */}
        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value as Priority)}
          className="w-full border px-4 py-2 rounded mb-4"
        >
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>

        {/* Comments Textarea */}
        <textarea
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          rows={4}
          className="w-full border px-4 py-2 rounded mb-4"
          placeholder="Comments"
        />

        {/* Buttons for closing or saving */}
        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded text-gray-700 hover:bg-gray-100"
          >
            Close
          </button>
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            {task.id ? 'Update' : 'Save'} 
          </button>
        </div>
      </div>
    </div>
  );
}


