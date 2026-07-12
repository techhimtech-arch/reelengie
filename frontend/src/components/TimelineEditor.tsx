import React from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  horizontalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Video, Image as ImageIcon } from 'lucide-react';

interface TimelineClip {
  scene: string;
  start: number;
  end: number;
  source_start?: number;
  media: string;
  media_type: string;
}

interface TimelineEditorProps {
  timeline: TimelineClip[];
  setTimeline: (t: TimelineClip[]) => void;
  projectId: string;
}

const SortableClip = ({ clip, projectId, id }: { clip: TimelineClip, projectId: string, id: string }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    width: `${Math.max(120, (clip.end - clip.start) * 25)}px`,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="h-32 bg-white/5 border border-white/10 rounded-lg overflow-hidden flex flex-col cursor-grab active:cursor-grabbing hover:border-primary/50 transition-colors shrink-0"
    >
      <div className="h-6 bg-black/40 px-2 flex items-center justify-between text-xs text-textMuted border-b border-white/10">
        <span className="truncate w-3/4">{clip.media}</span>
        <span className="flex items-center gap-1">
          {clip.media_type === 'video' ? <Video className="w-3 h-3" /> : <ImageIcon className="w-3 h-3" />}
        </span>
      </div>
      <div className="flex-1 relative">
        {clip.media_type === 'video' ? (
          <video 
            src={`http://127.0.0.1:8765/static/${projectId}/videos/${clip.media}`} 
            className="w-full h-full object-cover opacity-60" 
          />
        ) : (
          <img 
            src={`http://127.0.0.1:8765/static/${projectId}/photos/${clip.media}`} 
            className="w-full h-full object-cover opacity-60" 
            alt="media" 
          />
        )}
        <div className="absolute inset-0 flex flex-col items-center justify-center p-2 text-center pointer-events-none">
          <span className="bg-black/60 px-2 py-1 rounded text-xs font-semibold text-white mb-1">
            {clip.scene}
          </span>
          <span className="bg-primary/80 px-2 py-1 rounded text-xs font-semibold text-white">
            {(clip.end - clip.start).toFixed(1)}s
          </span>
        </div>
      </div>
    </div>
  );
};

export const TimelineEditor: React.FC<TimelineEditorProps> = ({ timeline, setTimeline, projectId }) => {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: any) => {
    const { active, over } = event;

    if (active.id !== over.id) {
      const oldIndex = timeline.findIndex(c => c.media === active.id);
      const newIndex = timeline.findIndex(c => c.media === over.id);

      const newTimeline = [...timeline];
      const media1 = newTimeline[oldIndex].media;
      const type1 = newTimeline[oldIndex].media_type;
      
      newTimeline[oldIndex].media = newTimeline[newIndex].media;
      newTimeline[oldIndex].media_type = newTimeline[newIndex].media_type;
      
      newTimeline[newIndex].media = media1;
      newTimeline[newIndex].media_type = type1;

      setTimeline(newTimeline);
    }
  };

  return (
    <div className="w-full overflow-x-auto pb-4">
      <div className="inline-flex min-w-full bg-black/20 p-4 rounded-xl border border-white/5">
        <DndContext 
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <div className="flex gap-2">
            <SortableContext 
              items={timeline.map(c => c.media)}
              strategy={horizontalListSortingStrategy}
            >
              {timeline.map((clip) => (
                <SortableClip 
                  key={clip.media}
                  id={clip.media}
                  clip={clip} 
                  projectId={projectId}
                />
              ))}
            </SortableContext>
          </div>
        </DndContext>
      </div>
    </div>
  );
};
