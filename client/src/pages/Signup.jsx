import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  phone: Yup.string()
    .matches(/^(07|01)\d{8}$/, "Invalid Kenyan phone number")
    .required("Phone required"),

  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password required"),

  estate: Yup.string().required("Estate required"),

  landmark: Yup.string().required("Landmark required")
});

function Signup() {

  function handleSubmit(values) {
    console.log("Signup data:", values);
  }

  return (

    <div>

      <h2>Signup</h2>

      <Formik
        initialValues={{
          phone:"",
          password:"",
          estate:"",
          landmark:""
        }}
        validationSchema={schema}
        onSubmit={handleSubmit}
      >

        <Form>

          <div>
            <label>Phone</label>
            <Field name="phone"/>
            <ErrorMessage name="phone"/>
          </div>

          <div>
            <label>Password</label>
            <Field type="password" name="password"/>
            <ErrorMessage name="password"/>
          </div>

          <div>
            <label>Estate</label>
            <Field name="estate"/>
            <ErrorMessage name="estate"/>
          </div>

          <div>
            <label>Nearby Landmark</label>
            <Field name="landmark"/>
            <ErrorMessage name="landmark"/>
          </div>

          <button type="submit">Signup</button>

        </Form>

      </Formik>

    </div>

  );
}

export default Signup; 