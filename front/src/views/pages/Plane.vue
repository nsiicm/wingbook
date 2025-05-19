<script setup>
import { PlaneService } from '@/service/PlaneService';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';

onMounted(() => {
    api.get('/planes').then((response) => (planes.value = response.data))
});

const toast = useToast();
const dt = ref();
const planes = ref();
const planeDialog = ref(false);
const deletePlaneDialog = ref(false);
const deleteplanesDialog = ref(false);
const plane = ref({});
const selectedplanes = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    plane.value = {};
    submitted.value = false;
    planeDialog.value = true;
}

function hideDialog() {
    planeDialog.value = false;
    submitted.value = false;
}

function saveplane() {
    submitted.value = true;
    if (plane.value.id) {
        const index = findIndexById(plane.value.id);
        planes.value[index] = { ...planes.value[index], ...plane.value };
        api.put(`/planes/${plane.value.id}/`, plane.value)
            .then(() => {
                planes.value[index] = plane.value;
                planeDialog.value = false;
                plane.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Plane Updated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update plane', life: 3000 });
            });
    } else
    {
    if (plane.value.registration_number && plane.value.model) { // Add validation for required fields
        api.post('/planes/', plane.value)
            .then((response) => {
                planes.value.push(response.data); // Add the newly created plane to the list
                planeDialog.value = false;
                plane.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Plane Created', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create plane', life: 3000 });
            });
    }
    }
}

function editPlane(prod) {
    plane.value = { ...prod };
    planeDialog.value = true;
}

function confirmDeletePlane(prod) {
    plane.value = prod;
    deletePlaneDialog.value = true;
}

function deleteplane() {
    api.delete(`/planes/${plane.value.id}/`)
        .then(() => {
            planes.value = planes.value.filter((val) => val.id !== plane.value.id);
            deletePlaneDialog.value = false;
            plane.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Plane Deleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete plane', life: 3000 });
        });
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < planes.value.length; i++) {
        if (planes.value[i].id === id) {
            index = i;
            break;
        }
    }

    return index;
}

function exportCSV() {
    dt.value.exportCSV();
}

function confirmDeleteSelected() {
    deleteplanesDialog.value = true;
}

function deleteSelectedplanes() {
    planes.value = planes.value.filter((val) => !selectedplanes.value.includes(val));
    deleteplanesDialog.value = false;
    selectedplanes.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'planes Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedplanes || !selectedplanes.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedplanes"
                :value="planes"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} planes"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage planes</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="id" header="Id" sortable style="min-width: 12rem"></Column>
                <Column field="model" header="Model" sortable style="min-width: 16rem"></Column>
                <Column field="registration_number" header="Registration" sortable style="min-width: 16rem"></Column>
                <Column field="single_engine" header="Single Engine" sortable style="min-width: 12rem">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.single_engine">Yes</span>
                        <span v-else>No</span>
                    </template>
                </Column>
                <Column field="single_pilot" header="Single Pilot" sortable style="min-width: 12rem">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.single_pilot">Yes</span>
                        <span v-else>No</span>
                    </template>
                </Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editPlane(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeletePlane(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="planeDialog" :style="{ width: '450px' }" header="plane Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="plane.image" :src="`https://primefaces.org/cdn/primevue/images/plane/${plane.image}`" :alt="plane.image" class="block m-auto pb-4" />
                <div>
                    <label for="registration_number" class="block font-bold mb-3">Registration</label>
                    <InputText id="registration_number" v-model.trim="plane.registration_number" required="true" autofocus :invalid="submitted && !plane.registration_number" fluid />
                    <small v-if="submitted && !plane.registration_number" class="text-red-500">Registration is required.</small>
                </div>
                <div>
                    <label for="model" class="block font-bold mb-3">model</label>
                    <InputText id="model" v-model="plane.model" required="true" rows="3" cols="20" fluid />
                </div>
                <div>
                    <label for="single_engine" class="block font-bold mb-3">Single Engine</label>
                    <InputSwitch id="single_engine" v-model="plane.single_engine" />
                </div>
                <div>
                    <label for="single_pilot" class="block font-bold mb-3">Single Pilot</label>
                    <InputSwitch id="single_pilot" v-model="plane.single_pilot" />
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveplane" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deletePlaneDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="plane"
                    >Are you sure you want to delete <b>{{ plane.registration_number }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteplaneDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteplane" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteplanesDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="plane">Are you sure you want to delete the selected planes?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteplanesDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedplanes" />
            </template>
        </Dialog>
    </div>
</template>
