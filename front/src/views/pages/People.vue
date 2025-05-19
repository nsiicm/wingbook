<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';

onMounted(() => {
    api.get('/people/').then((response) => (persons.value = response.data))
});

const toast = useToast();
const dt = ref();
const persons = ref();
const personDialog = ref(false);
const deletePersonDialog = ref(false);
const deletepersonsDialog = ref(false);
const person = ref({});
const selectedpersons = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    person.value = {};
    submitted.value = false;
    personDialog.value = true;
}

function hideDialog() {
    personDialog.value = false;
    submitted.value = false;
}

function saveperson() {
    submitted.value = true;
    if (person.value.id) {
        const index = findIndexById(person.value.id);
        persons.value[index] = { ...persons.value[index], ...person.value };
        api.put(`/people/${person.value.id}/`, person.value)
            .then(() => {
                persons.value[index] = person.value;
                personDialog.value = false;
                person.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'PersonUpdated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update person', life: 3000 });
            });
    } else
    {
    if (person.value.first_name && person.value.model) { // Add validation for required fields
        api.post('/people/', person.value)
            .then((response) => {
                persons.value.push(response.data); // Add the newly created person to the list
                personDialog.value = false;
                person.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'PersonCreated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create person', life: 3000 });
            });
    }
    }
}

function editPerson(prod) {
    person.value = { ...prod };
    personDialog.value = true;
}

function confirmDeletePerson(prod) {
    person.value = prod;
    deletePersonDialog.value = true;
}

function deleteperson() {
    api.delete(`/people/${person.value.id}/`)
        .then(() => {
            persons.value = persons.value.filter((val) => val.id !== person.value.id);
            deletePersonDialog.value = false;
            person.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'PersonDeleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete person', life: 3000 });
        });
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < persons.value.length; i++) {
        if (persons.value[i].id === id) {
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
    deletepersonsDialog.value = true;
}

function deleteSelectedpersons() {
    persons.value = persons.value.filter((val) => !selectedpersons.value.includes(val));
    deletepersonsDialog.value = false;
    selectedpersons.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'persons Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedpersons || !selectedpersons.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedpersons"
                :value="persons"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} persons"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage persons</h4>
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
                <Column field="first_name" header="First Name" sortable style="min-width: 16rem"></Column>
                <Column field="last_name" header="Last Name" sortable style="min-width: 16rem"></Column>
                <Column field="is_pilot" header="Is Pilot" sortable style="min-width: 16rem">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.is_pilot">Yes</span>
                        <span v-else>No</span>
                    </template>
                </Column>
                <Column field="is_instructor" header="Is Instructor" sortable style="min-width: 16rem">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.is_instructor">Yes</span>
                        <span v-else>No</span>
                    </template>
                </Column>
                <Column field="is_main_pilot" header="Is Main Pilot" sortable style="min-width: 16rem">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.is_main_pilot">Yes</span>
                        <span v-else>No</span>
                    </template>
                </Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editPerson(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeletePerson(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="personDialog" :style="{ width: '450px' }" header="person Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="person.image" :src="`https://primefaces.org/cdn/primevue/images/person/${person.image}`" :alt="person.image" class="block m-auto pb-4" />
                <div>
                    <label for="first_name" class="block font-bold mb-3">First Name</label>
                    <InputText id="first_name" v-model.trim="person.first_name" required="true" autofocus :invalid="submitted && !person.first_name" fluid />
                    <small v-if="submitted && !person.first_name" class="text-red-500">Registration is required.</small>
                </div>
                <div>
                    <label for="last_name" class="block font-bold mb-3">Last Name</label>
                    <InputText id="last_name" v-model="person.last_name" required="true" rows="3" cols="20" fluid />
                </div>
                <div>
                    <label for="is_pilot" class="block dont-bold mb-3"> Is Pilot </label>
                    <InputSwitch id="is_pilot" v-model="person.is_pilot" />
                </div>
                <div>
                    <label for="is_instructor" class="block dont-bold mb-3"> Is Instructor </label>
                    <InputSwitch id="is_instructor" v-model="person.is_instructor" />
                </div>
                <div>
                    <label for="is_main_pilot" class="block dont-bold mb-3"> Is Main Pilot </label>
                    <InputSwitch id="is_main_pilot" v-model="person.is_main_pilot" />
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveperson" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deletePersonDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="person"
                    >Are you sure you want to delete <b>{{ person.first_name }} {{ person.last_name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deletepersonDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteperson" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deletepersonsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="person">Are you sure you want to delete the selected persons?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deletepersonsDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedpersons" />
            </template>
        </Dialog>
    </div>
</template>
