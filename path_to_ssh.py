

def movement_to_vector(self):
    for i in range(len(self.move_list)):
        x_inital = self.move_list[i][0]
        y_inital = self.move_list[i][1]
        z_inital = self.move_list[i][2]

        x_final = self.move_list[i+1][0]
        y_final = self.move_list[i+1][1]
        z_final = self.move_list[i+1][2]

        movement_list = []
        movement_list.append
def path_2_ssh(self):
    direct_code = []
    # check if initial rotation needs to take place
    if self.rotation != self.move_list[0][1]:
        # rotation of robot not correct
        direct_code.append(self.change_rotation(self, self.move_list[i][1]))
    elif self.rotation == self.move_list[0][1]:
        direct_code.append(0)
    # find number of gaps between
    # check the i and i+1 rotation are the same
    for i in range(len(self.move_list)):
        if self.move_list[i][1] == self.move_list[1+i][1]:
            # no rotation change between moves i and i+1
            pass
        elif self.move_list[i][1] != self.move_list[1+i][1]:
            self.change_rotation(self, )



