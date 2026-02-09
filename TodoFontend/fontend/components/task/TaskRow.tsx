'use client';

import { Task } from '@/types/task';
import PriorityBadge from './PriorityBadge';
import '@/styles/tasktable&row.css'

type Props = {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (id: number) => void;
  onComplete?: (id: number) => void;
  onUndo?: (id: number) => void;
};

export default function TaskRow({
  task,
  onEdit,
  onDelete,
  onComplete,
  onUndo,
}: Props) {
  return (
    <tr
      className={`border-b transition-colors duration-200
        ${task.completed ? 'bg-gray-50 text-gray-400' : 'hover:bg-gray-100'}
      `}
      onClick={() => onEdit?.(task)}  // Using optional chaining to call onEdit only if it's defined
    >
      {/* Title */}
      <td className="p-3 font-medium">
        <span className={task.completed ? 'line-through' : ''}>
          {task.title}
        </span>
      </td>

      {/* Deadline */}
      <td className="p-3 text-sm">
        {task.deadline || <span className="text-gray-400">—</span>}
      </td>

      {/* Priority */}
      <td className="p-3">
        <PriorityBadge priority={task.priority} />
      </td>

      {/* Actions */}
      <td className="p-3 flex justify-end gap-3 text-sm">
        {!task.completed && onComplete && (
          <button
            onClick={(e) => { e.stopPropagation(); onComplete?.(task.id); }}  // Optional chaining for onComplete
            className="rounded-md px-3 py-1 text-green-700 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Complete
          </button>
        )}

        {task.completed && onUndo && (
          <button
            onClick={(e) => { e.stopPropagation(); onUndo?.(task.id); }}  // Optional chaining for onUndo
            className="rounded-md px-3 py-1 text-indigo-700 hover:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Undo
          </button>
        )}

        {onEdit && (
          <button
            onClick={(e) => { e.stopPropagation(); onEdit?.(task); }}  // Optional chaining for onEdit
            className="rounded-md px-3 py-1 text-blue-700 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Edit
          </button>
        )}

        {onDelete && (
          <button
            onClick={(e) => { e.stopPropagation(); onDelete?.(task.id); }}  // Optional chaining for onDelete
            className="rounded-md px-3 py-1 text-red-700 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Delete
          </button>
        )}
      </td>
    </tr>
  );
}
