# As a User


## Register
user can register for an account in top right options

![Register - option](/testing/user/Register-Option.png)

This opens a page to enter details to create an account. Since this uses allauth it has validation for emails and weak passwords etc by default.

![Register - Page](/testing/user/Register-page.png)

After an account is made, it sends an email to verify the account before you can use it

![Register - Verify](/testing/user/Register-Verify.png)

Email shown here for verification

![Register - Verification Email](/testing/user/Register-Verificationemail.png)

Clicking link in email takes you to this page that then when pressed, verifys the account and allows logging in.

![Register - Verified](/testing/user/Register-verified.png)

## Login

When an account is verified, it can be logged into in the login page like this

![Login - Page](/testing/user/LogIn-Page.png)

Once logged in, the top right of the screen shows your account name and you then have the ability to suggested ideas, edit account settings and do admin things if you are an admin.

![Loggedin](/testing/user/Loggedin.png)

## Reset password

Allauth comes with a simple password reset system that sends an email to the user to then change their password, this is all default system so it just works.

![Password - ResetPage](/testing/user/Password-ResetPage.png)

![Password - ResetEmail](/testing/user/Password-ResetEmail.png)

## enable/disable emails

On the user settings page there is a toggle for recieving email notifications, this can be saved and is respected when updates are created.

![EmailSetting - Visible](/testing/user/EmailSetting-Visible.png)

![EmailSetting - Saves](/testing/user/EmailSetting-SavesWhenChanged.png)

## leave comments

When logged in you can post comments on any project, example comment before being posted here

![Comment - Before](/testing/user/Comment-Before.png)

And then once the comment is posted, it appears below the project permanently.

![Comment - after](/testing/user/Comment-after.png)

## View Details on a given project

When you click on an item in the menu it opens a view of specifically that item that states who suggested it and if its funded then the fund button dissapears and it instead lists who funded it.

![Project - view](/testing/user/Project-view.png)

## View Comments

One Comment and then multiple comments displayed at once, can be viewed when not logged in

![Comment - view one](/testing/user/comment-persists.png)

![Comment - view multiple](/testing/user/comment-multiple.png)

# As a browser

## View all projects

Project view lists all projects

![Projects - View all](/testing/Browser/ViewAll.png)

## Sort projects

### Options available to view in varying orders, shown here are

category A-Z

![Projects - sort category](/testing/Browser/sortCategory.png)

category Z-A

![Projects - sort categoryreverse](/testing/Browser/sortReverseCategory.png)

price low to high

![Projects - sort price](/testing/Browser/sortPrice.png)

price high to low 

![Projects - sort price](/testing/Browser/sortInversePrice.png)

### There are also options to filter down by category at top of screen

![Projects - filter category options](/testing/Browser/FilterCategoryOptions.png)

when filtered it only shows items of that category.

![Projects - filter category](/testing/Browser/FilterCategory.png)

## Search projects

Search bar at top of screen allows searching for keywords. 

Searching for "draw" brings both things with draw in the title

![Projects - Search Draw](/testing/Browser/SearchDraw.png)

Searching "wall" brings up the fox since in its description is the word "wall".

![Projects - Search Wall](/testing/Browser/SearchWall.png)

# As a Suggester

## Suggest a project

Users when logged in can get a form to suggest a project. They can give preliminary settings for a timeframe and what category it is, and based on the two, a price estimate will be automatically filled in. 

![Project - Suggest Page](/testing/Suggester/SuggestForm.png)

This price adjusts as you change those settings, here it is with a different price after the settings were adjusted.

![Project - Suggest price](/testing/Suggester/SuggestDifferentPrice.png)

These prices are re-calcalated when actually adding to the database, it is not possible for the user to change it and have that effect anything.

When an idea is submitted, it is not immediately added to the full public viewing as it needs to be curated, so it does not immediately show in the listing, but a popup shows up to tell that it will be reviewed.

![Project - Suggest not added yet](/testing/Suggester/suggestnotadded.png)

## view all projects i've suggested

In the users profile page, there is an option to display every project they have suggested.

![View - all suggested](/testing/Suggester/CanSeeAllSuggested.png)

## view updates on projects i've suggested

Special to projects suggested by you, there is the ability to view updates, this can be viewed in the list view or directly on each item

![View - updates](/testing/Suggester/SuggestUpdates.png)

## recieve email updates on projects i've suggested

An email is sent each time an update is made.

![View - email](/testing/Suggester/SuggestUpdateEmail.png)

# As a Funder

## Fund a project

To fund an item, user enters in data for payment 

![Fund - enter data](/testing/Funder/Funding-EnterData.png)

Since it uses stripe, card detail validation is automatically handled.

![Fund - invalid](/testing/Funder/Funding-InvalidData.png)

Once a payment is processed user is taken to the final checkout page.

![Fund - checkout](/testing/Funder/Checkoutpage.png)


## Safely pay for funding with card and know that my purchase went through

An email is sent to confirm the project is funded (and notification is also sent to the suggester)

![Fund - confirmation](/testing/Funder/Funding-Confirmation.png)

Stripe webhooks will go through and nothing will happen if payment went through fine

![Fund - Already](/testing/Funder/PaymentAlreadyIn.png)

If i delete the order through the admin pages 

![Fund delete](/testing/Funder/deletepayment.png)

And then re-force the stripe webhook, the payment will be re-added to the list and everything will work as before

![Fund readded](/testing/Funder/Fundre-added.png)

![Fund readded](/testing/Funder/canstillseeeverything.png)

## View all projects i've funded

A list of all funded projects is visible just like with suggested

![All Funded](/testing/Funder/ViewAll.png)


## view updates on projects i've funded

Updates are viewable for all funded projects same as for suggested projects.

![Updates viewable](/testing/Funder/Funding-UpdatesViewable.png)

![Updates](/testing/Funder/Update-ViewUpdates.png)

# As an Admin

## Edit a project thats already up

Admins have the ability to edit any details of a project.

![edit before](/testing/Admin/EditBefore.png)

![edit during](/testing/Admin/editduring.png)

![edit after](/testing/Admin/editafter.png)

This automatically generates an update for that project that will message the suggester and the funder that the changes occured and details what was changed.

![edit update](/testing/Admin/editupdate.png)

## approve not yet approved projects so they are visible to all users

Approving is just the same as editting, its just special in that it adds the ability for normal users to view it and fund it.

![approve option](/testing/Admin/ApproveProjectView.png)

![approve option](/testing/Admin/CanApprove.png)

![approve option](/testing/Admin/OnceApprovedCanFund.png)

This produces a special version of the notification telling you where to find the project after its approved

![approved](/testing/Admin/approved.png)

## Delete bad projects

Admins have a delete button available that deletes projects, this doesnt delete the updates/funding of it.

![delete before](/testing/Admin/deletebefore.png)

![delete after](/testing/Admin/deleteafter.png)

## Currate comments/delete comments

Admins have a delete button available that deletes projects, this doesnt delete the updates/funding of it.

![delete comment before](/testing/Admin/Comment-BeforeDelete.png)

![delete comment](/testing/Admin/Comment-Delete.png)

![delete comment after](/testing/Admin/Comment-AfterDelete.png)


## Send Project updates out

There is a interface on every project to create an update that sends an email if appropriate.

![update](/testing/Admin/updateFormFilledIn.png)

![update](/testing/Admin/UpdateStored.png.png)


# Actual Email Handling since django natively does email system

Emailing was added proper late since it was a couple line edit that django full handled, so here is a screenshot the email actually being recieved through Gmail

![Actual Email](/testing/actualEmail.png)

![Other Actual Email](/testing/ActualEmail2.png)