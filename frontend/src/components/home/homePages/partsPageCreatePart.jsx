import React, { useState } from "react";
import { TextField, Button, MenuItem, Select, InputLabel, FormControl, Grid, Typography } from "@mui/material";

const CreatePartComponent = ({ userInfo,fetchParthData,tabValue, partTypes, airplaneTypes }) => {
  const [partType, setPartType] = useState("");
  const [airplaneType, setUavType] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/parts/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "airplane_type": airplaneType,
          "part_type": partType
        }),
      });
    } catch (error) {
      alert("Bir hata oluştu.");
    }

    setIsSubmitting(false);
    fetchParthData(tabValue); // envanter güncellenir
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={4}>
          <FormControl fullWidth>
            <InputLabel>Parça Tipi</InputLabel>
            <Select
              value={partType}
              onChange={(e) => setPartType(e.target.value)}
              variant="standard"
            >
              {partTypes
                .map((type) => (
                  <MenuItem key={type.id} value={type.id} disabled={userInfo?.team?.part_type_id !== type.id && !userInfo?.isAdmin }>
                    {type.name} 
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={4}>
          <FormControl fullWidth>
            <InputLabel>Uçak</InputLabel>
            <Select
              value={airplaneType}
              variant="standard"
              onChange={(e) => setUavType(e.target.value)}
            >
              {airplaneTypes.map((type) => (
                <MenuItem key={type.id} value={type.id} disabled={ !userInfo?.team?.part_type_id && !userInfo?.isAdmin }>
                  {type.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Button type="submit" variant="contained" color="secondary" disabled={isSubmitting || !airplaneType || !partType || !(userInfo?.isAdmin || userInfo?.team?.part_type_id)} fullWidth>
            {isSubmitting ? "Parça Oluşturuluyor..." : "Parçayı Oluştur"}
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default CreatePartComponent;
