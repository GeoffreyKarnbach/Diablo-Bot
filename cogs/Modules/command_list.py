commands_per_level = [
                    [("rephelp","List of commands you can use.")],
                    [("repcheck","<user ID / @User> : Checks the reputation of the given user."),("prep","<user ID / @User> <reason> : Gives a reputation point."),("mrep","<user ID / @User> <reason> : Removes a reputation point."),("repedit","Edit reason on last reputation point.")],
                    [("mrepcheck","<user ID / @User> : Extended version of repcheck (moderator version)"),("mlockulist","List of all locked users.")],
                    [("mlocku","<user ID / @User> <reason>: Locks/ unlocks a specific user from the reputation system.")],
                    [("mdayreset","<user ID / @User> <reason>: Resets the given points counter for the specific user today.")],
                    [("mrepdel","<user ID / @User> <repid> <reason> Delete the specific reputation with given ID."),("mrepedit","<repid> <repType> <text> Modifies the reason of the given reputation.")],
                    [("mnuke","<user ID / @User> <reason> Deletes all the reputations from a specific user.")],
                    [
                        ("acmdlist","List of all cmd channels."),
                        ("acmdadd","<channel ID>: Adds the given channel to the cmd list."),
                        ("acmddel","<channel ID>: Removes the given channel from the cmd list."),
                        ("asetminchar","<value>: Sets the minimum value of any reason (mrep/prep) string."),
                        ("asetmaxchar","<value>: Sets the maximum value of any reason (mrep/prep) string."),
                        ("asetulogs","<channel ID>: Adds the given channel to the user log channel list."),
                        ("asetmlogs","<channel ID>: Adds the given channel to the moderator log channel list."),
                        ("asetalogs","<channel ID>: Adds the given channel to the admin log channel list."),
                        ("asetologs","<channel ID>: Adds the given channel to the owner log channel list."),
                        ("alogsdel","<channel ID>: Removes the given channel globally as log channel."),
                        ("alogslist","List of all logs channel and their usage (u, m, a)."),
                        ("aprep","<user ID> <reason>: Gives a specific admin reputation point (blue)."),
                        ("amrep","<user ID> <reason>: Removes a reputation point."),
                        ("araid"," Enables/ Disables raid mode."),
                        ("adhelpchannel","<channel ID> : Sets the help channel to be shown in rephelp."),
                        ("amodlist","Shows the list of all roles and their authorization level."),
                        ("aroleadd","<role ID> <value>: Gives number of points that can be given by the specified role."),
                        ("aroledel","<role ID>: Resets the number of points the role can give."),
                        ("arolelock","<role ID>: Locks/ Unlocks a specific role from getting/giving reputation points."),
                        ("arolelocklist","List of all locked roles."),
                        ("arolelist","List of all giveable points per role.")
                    ],

                    [("oprefix","<prefix>: Sets the new prefix as default bot prefix."),("orolelvl","<role ID> <value>: Gives a certain authorization level to role."),("odelrolelvl","<role ID>: Deletes authorization level for specific role."),("oroleban","<role ID>: Sets a specific role to level 0."),("odelroleban","<role ID>: Removes level 0 from specific role.")]
                    ]