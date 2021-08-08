import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  Grid,
  Typography,
} from "@material-ui/core";
import { FormatListBulletedSharp } from "@material-ui/icons";
import axios from "axios";
import React, { Component } from "react";
import { useRef } from "react";
import { useEffect } from "react";
import { useState } from "react";
import { useCookies } from "react-cookie";
import root_url from "../config";

const CustomCheckbox = ({ isChecked, content, setSkill }) => {
  const [checked, setChecked] = useState(isChecked);
  const handleChange = (event) => {
    setChecked(event.target.checked);
    if (event.target.checked) {
      setSkill(content, true);
    } else {
      setSkill(content, false);
    }
  };
  return (
    <>
      <Checkbox
        color="primary"
        checked={checked}
        onChange={handleChange}
      ></Checkbox>
    </>
  );
};

const renderCheckbox = (isChecked, content, setSkill) => {
  // if (isChecked === true) {
  //   return <Checkbox color="primary" checked={true}></Checkbox>;
  // } else {
  //   return <Checkbox color="primary"></Checkbox>;
  // }

  if (isChecked === true) {
    console.log("Render checkbox");
    return (
      <CustomCheckbox isChecked={true} content={content} setSkill={setSkill} />
    );
  } else {
    return (
      <CustomCheckbox isChecked={false} content={content} setSkill={setSkill} />
    );
  }
};

const renderSkillItem = (skillName, existedSkills, setSkill) => {
  if (existedSkills.includes(skillName)) {
    console.log(skillName);
    return (
      <ListItem key={skillName}>
        {renderCheckbox(true, skillName, setSkill)}
        <ListItemText>{skillName}</ListItemText>
      </ListItem>
    );
  }

  return (
    <ListItem>
      {renderCheckbox(false, skillName, setSkill)}
      <ListItemText>{skillName}</ListItemText>
    </ListItem>
  );
};

const renderGroupSkill = (groupName, skillList, existedSkills, setSkill) => {
  return (
    <Grid item xs={12} md={6}>
      <Typography variant="h6">{groupName}</Typography>
      <List>
        {skillList.map((item) => {
          return renderSkillItem(item, existedSkills, setSkill);
        })}
      </List>
    </Grid>
  );
};

export default function DialogSkill({ isOpen, closeDialog, isUpdate }) {
  const [knowledge, setKnowledge] = useState([]);
  const [technicalSkill, setTechnicalSkill] = useState([]);
  const [technology, setTechnology] = useState([]);
  const [cookies, setCookie] = useCookies(["user"]);
  const [existedSkills, setExistedSkills] = useState([]);

  const handleUpdate = () => {
    const user_id = cookies.user;
    var request = {};
    request["user_id"] = user_id;
    request["user_skills"] = [];
    for (var i = 0; i < existedSkills.length; i++) {
      request["user_skills"].push(existedSkills[i]);
    }

    axios.post(root_url + "/api/user/skills", request);
    const channel = new BroadcastChannel("app-data");
    channel.postMessage({ is_update_skills: true });
  };

  const renderActionButtons = () => {
    return (
      <>
        <Button onClick={closeDialog}>Cancel</Button>
        <Button color="primary" onClick={handleUpdate}>
          Update
        </Button>
      </>
    );
  };

  const setSkill = (skill, status) => {
    if (status) {
      setExistedSkills([...existedSkills, skill]);
    } else {
      const arr_copy = [...existedSkills];
      setExistedSkills(arr_copy.filter((item) => item !== skill));
    }
  };

  useEffect(() => {
    const knowledge_temp = [];
    const technical_skill_temp = [];
    const tech_temp = [];
    axios
      .get(root_url + "/api/skills")
      .then((response) => {
        for (var i = 0; i < response.data.length; i++) {
          if (response.data[i].type === "Knowledge") {
            knowledge_temp.push(response.data[i].name);
          }

          if (response.data[i].type === "TechnicalSkill") {
            technical_skill_temp.push(response.data[i].name);
          }

          if (response.data[i].type === "Technology") {
            tech_temp.push(response.data[i].name);
          }
        }
      })
      .then(() => {
        setKnowledge(knowledge_temp);
        setTechnology(tech_temp);
        setTechnicalSkill(technical_skill_temp);
      });

    // Check user skills
    if (isUpdate === true) {
      const user_id = cookies.user;
      console.log("Get skills of the current user");
      console.log(user_id);
      axios.get(root_url + "/api/" + user_id + "/skills").then((res) => {
        const skills = [];
        for (var i = 0; i < res["data"].length; i++) {
          skills.push(res["data"][i]["skill_name"]);
        }
        setExistedSkills(skills);
      });
    }
  }, []);

  console.log("Reload");
  console.log(existedSkills);

  return (
    <>
      <Dialog
        maxWidth="sm"
        open={isOpen}
        aria-labelledby="simple-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle>Add existed skills</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Add your existed skills to provide the best career path for you.
          </DialogContentText>
          <Grid container spacing={2}>
            {renderGroupSkill(
              "Technical skill",
              technicalSkill,
              existedSkills,
              setSkill
            )}
            {renderGroupSkill("Knowledge", knowledge, existedSkills, setSkill)}
            {renderGroupSkill(
              "Technology",
              technology,
              existedSkills,
              setSkill
            )}
          </Grid>
        </DialogContent>
        <DialogActions>{renderActionButtons()}</DialogActions>
      </Dialog>
    </>
  );
}
