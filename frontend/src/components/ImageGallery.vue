<template xmlns="http://www.w3.org/1999/html">
  <div>
    <VueDraggableNext class="grid grid-cols-6 gap-4" :list="props.images" v-bind="dragOptions">
      <div v-for="image in props.images" :key="image.id" class="hover:bg-slate-10">
        <div class="aspect-w-5 aspect-h-3 w-full overflow-hidden">
          <img :src="image.image_url" class="rounded hover:transparency-80 h-full w-full object-cover object-center" />
        </div>
        <div class="rounded mt-1 text-center">
          <button @click.prevent="deleteImage(image.id)" class="inline-flex justify-center rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-rose-600 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2">Delete</button>
        </div>
      </div>
    </VueDraggableNext>
  </div>
</template>

<script setup lang="ts">
import { VueDraggableNext } from 'vue-draggable-next'

const props = defineProps({
  images: { type: Object, required: true },
  onDelete: { type: Function, required: true }
})

const dragOptions = {
  animation: 200,
  group: "description",
  disabled: false,
  ghostClass: "ghost"
};

function deleteImage(imageId: string) {
  console.log('Deleting image: ' + imageId);
  props.onDelete(imageId);
}

</script>