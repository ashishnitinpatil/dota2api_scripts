from django.db import models

# Create your models here.

class match_history(models.Model):
    """Model to save any match history results"""

    req_status_choices = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    req_open = models.CharField(default="O", choices=req_status_choices,
                                max_length=2, verbose_name="Request Status",
                                help_text="Status of the request")

    contact_number = models.CharField(blank=True, null=True, max_length=16,
                                      help_text="Contact number (optional)")

    gender_req_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'Any'),
    )
    gender_req = models.CharField(default="A", choices=gender_req_choices,
                                  max_length=2, help_text="Gender requirement",
                                  verbose_name="Gender requirement")

    locality = models.CharField(null=True, max_length=64, help_text="Name of locality/society")
    rent = models.IntegerField(null=True, help_text="Rent per month (in Rs.)")
    deposit = models.IntegerField(null=True, help_text="Security deposit (in Rs.)")
    vacancies = models.IntegerField(default=1, help_text="Total vacancies (no. of persons)")
    immediate_possession = models.BooleanField(default=True, help_text="Is the room available for immediate possession?")
    available_from = models.DateField(blank=True, null=True, help_text="When would the room be available for accomodation?")
    more_details = models.CharField(blank=True, null=True, max_length=2048, help_text="Additional details")

    modified_on = models.DateTimeField(blank=True, null=True, auto_now_add=True, help_text="Internal field")

    # default manager
    objects = models.Manager()
    # custom manager for filtering of "closed" & "old but open" posts
    active = RoomManager()

    def __unicode__(self):
        return "{0} - {1}".format(self.locality, self.owner.username)

    def get_post_url(self):
        return reverse('roomreq:indi', kwargs={'post_id':self.id})

    def save(self, *args, **kwargs):
        if not self.immediate_possession and not self.available_from:
            self.available_from = get_next_month_first_date()
        self.modified_on = datetime.datetime.today().date()
        super(room_requirement, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Room Requirement"
        ordering = ['-modified_on',]
