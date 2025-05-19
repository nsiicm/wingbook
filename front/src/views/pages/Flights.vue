<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';

onMounted(() => {
    api.get('/flights/').then((response) => (flights.value = response.data))
});

const toast = useToast();
const dt = ref();
const flights = ref();
const flightDialog = ref(false);
const deleteFlightDialog = ref(false);
const deleteflightsDialog = ref(false);
const flight = ref({});
const selectedflights = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    flight.value = {};
    submitted.value = false;
    flightDialog.value = true;
}

function hideDialog() {
    flightDialog.value = false;
    submitted.value = false;
}

function saveflight() {
    submitted.value = true;
    if (flight.value.id) {
        const index = findIndexById(flight.value.id);
        flights.value[index] = { ...flights.value[index], ...flight.value };
        api.put(`/people/${flight.value.id}/`, flight.value)
            .then(() => {
                flights.value[index] = flight.value;
                flightDialog.value = false;
                flight.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightUpdated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update flight', life: 3000 });
            });
    } else
    {
    if (flight.value.first_name && flight.value.model) { // Add validation for required fields
        api.post('/people/', flight.value)
            .then((response) => {
                flights.value.push(response.data); // Add the newly created flight to the list
                flightDialog.value = false;
                flight.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightCreated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create flight', life: 3000 });
            });
    }
    }
}

function editFlight(prod) {
    flight.value = { ...prod };
    flightDialog.value = true;
}

function confirmDeleteFlight(prod) {
    flight.value = prod;
    deleteFlightDialog.value = true;
}

function deleteflight() {
    api.delete(`/people/${flight.value.id}/`)
        .then(() => {
            flights.value = flights.value.filter((val) => val.id !== flight.value.id);
            deleteFlightDialog.value = false;
            flight.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightDeleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete flight', life: 3000 });
        });
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < flights.value.length; i++) {
        if (flights.value[i].id === id) {
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
    deleteflightsDialog.value = true;
}

function deleteSelectedflights() {
    flights.value = flights.value.filter((val) => !selectedflights.value.includes(val));
    deleteflightsDialog.value = false;
    selectedflights.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'flights Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedflights || !selectedflights.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedflights"
                :value="flights"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} flights"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage flights</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="id" header="Id" sortable style="min-width: 4rem"></Column>
                <Column field="date" header="Date" sortable style="min-width: 8rem"></Column>
                <Column field="departure_airport" header="Departure Airport" sortable style="min-width: 6rem"></Column>
                <Column field="departure_time" header="Departure Time" sortable style="min-width: 6rem"></Column>
                <Column field="arrival_airport" header="Arrival Airport" sortable style="min-width: 6rem"></Column>
                <Column field="arrival_time" header="Arrival Time" sortable style="min-width: 6rem"></Column>
                <Column field="plane.model" header="Plane" sortable style="min-width: 10rem"></Column>
                <Column field="plane.registration_number" header="Registration" sortable style="min-width: 8rem"></Column>
                <Column field="se_duration" header="Single Engine Duration" sortable style="min-width: 6rem"></Column>
                <Column field="me_duration" header="Multi Engine Duration" sortable style="min-width: 6rem"></Column>
                <Column field="multi_pilot_duration" header="Multi Pilot Duration" sortable style="min-width: 6rem"></Column>
                <Column field="flight_duration" header="Flight Duration" sortable style="min-width: 6rem"></Column>
                <Column field="pilot_in_command.last_name" header="Pilot" sortable style="min-width: 12rem"></Column>
                <Column field="landing_day_num" header="Landing Day" sortable style="min-width: 6rem"></Column>
                <Column field="landing_night_num" header="Landing Night" sortable style="min-width: 6rem"></Column>
                <Column field="ifr_apch_num" header="IFR Approach" sortable style="min-width: 6rem"></Column>
                <Column field="night_duration" header="Night Duration" sortable style="min-width: 6rem"></Column>
                <Column field="ifr_duration" header="IFR Duration" sortable style="min-width: 6rem"></Column>
                <Column field="pilot_in_command_duration" header="Pilot in Command Duration" sortable style="min-width: 6rem"></Column>
                <Column field="copilot_duration" header="Co-Pilot Duration" sortable style="min-width: 6rem"></Column>
                <Column field="dual_duration" header="Dual Duration" sortable style="min-width: 6rem"></Column>
                <Column field="instructor_duration" header="Instructor Duration" sortable style="min-width: 6rem"></Column>
                <Column field="simulator_date" header="Simulator Date" sortable style="min-width: 6rem"></Column>
                <Column field="simulator_type" header="Simulator Type" sortable style="min-width: 12rem"></Column>
                <Column field="simulator_duration" header="Simulator Duration" sortable style="min-width: 6rem"></Column>
                <Column field="comments" header="Comments" sortable style="min-width: 12rem"></Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editFlight(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteFlight(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="flightDialog" :style="{ width: '450px' }" header="flight Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="flight.image" :src="`https://primefaces.org/cdn/primevue/images/flight/${flight.image}`" :alt="flight.image" class="block m-auto pb-4" />
                <div>
                    <label for="date" class="block font-bold mb-3">Date</label>
                    <DatePicker :showIcon="true" :showButtonBar="true" v-model="calendarValue"></DatePicker>
                </div>
                <div>
                    <label for="departure_airport" class="block font-bold mb-3">Departure Airport</label>
                    <InputText id="departure_airport" v-model.trim="flight.departure_airport" required="true" autofocus :invalid="submitted && !flight.departure_airport" fluid />
                </div>
                <div>
                    <label for="departure_time" class="block font-bold mb-3">Departure Time</label>
                    <TimePicker id="departure_time" v-model="flight.departure_time" :showIcon="true" :hourFormat="24" required="true" autofocus :invalid="submitted && !flight.departure_time" />
                </div>
                <div>
                    <label for="arrival_airport" class="block font-bold mb-3">Arrival Airport</label>
                    <InputText id="arrival_airport" v-model.trim="flight.arrival_airport" required="true" autofocus :invalid="submitted && !flight.arrival_airport" fluid />
                </div>
                <div>
                    <label for="arrival_time" class="block font-bold mb-3">Arrival Time</label>
                    <InputText id="arrival_time" v-model.trim="flight.arrival_time" required="true" autofocus :invalid="submitted && !flight.arrival_time" fluid />
                </div>
                <div>
                    <label for="first_name" class="block font-bold mb-3">First Name</label>
                    <InputText id="first_name" v-model.trim="flight.first_name" required="true" autofocus :invalid="submitted && !flight.first_name" fluid />
                    <small v-if="submitted && !flight.first_name" class="text-red-500">Registration is required.</small>
                </div>
                <div>
                    <label for="last_name" class="block font-bold mb-3">Last Name</label>
                    <InputText id="last_name" v-model="flight.last_name" required="true" rows="3" cols="20" fluid />
                </div>
                <div>
                    <label for="is_pilot" class="block dont-bold mb-3"> Is Pilot </label>
                    <InputSwitch id="is_pilot" v-model="flight.is_pilot" />
                </div>
                <div>
                    <label for="is_instructor" class="block dont-bold mb-3"> Is Instructor </label>
                    <InputSwitch id="is_instructor" v-model="flight.is_instructor" />
                </div>
                <div>
                    <label for="is_main_pilot" class="block dont-bold mb-3"> Is Main Pilot </label>
                    <InputSwitch id="is_main_pilot" v-model="flight.is_main_pilot" />
                </div>
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveflight" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteFlightDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="flight"
                    >Are you sure you want to delete <b>{{ flight.first_name }} {{ flight.last_name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteflightDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteflight" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteflightsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="flight">Are you sure you want to delete the selected flights?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteflightsDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedflights" />
            </template>
        </Dialog>
    </div>
</template>
